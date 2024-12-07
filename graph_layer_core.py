from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Set, Union, Optional
from enum import Enum
import uuid

class EntityType(Enum):
    STANDARD = "standard"
    PROPERTY = "property"

@dataclass(frozen=True)
class EntityId:
    """
    Unique identifier for an entity or property.
    Similar to Wikidata's Q-numbers and P-numbers.
    """
    id_type: EntityType
    local_id: str
    node_id: str  # ID of the node that created this entity
    
    def __str__(self):
        prefix = "P" if self.id_type == EntityType.PROPERTY else "Q"
        return f"{prefix}{self.local_id}@{self.node_id}"

@dataclass
class Entity:
    """
    Represents any item in the system.
    Uses a CRDT set for labels and descriptions to handle concurrent modifications.
    """
    id: EntityId
    created_at: datetime
    tombstone: bool = False  # For soft deletion
    
    # CRDT for labels in different languages
    labels: Dict[str, Set[tuple[str, datetime, str]]] = field(default_factory=dict)
    # CRDT for descriptions in different languages
    descriptions: Dict[str, Set[tuple[str, datetime, str]]] = field(default_factory=dict)

@dataclass(frozen=True)
class Statement:
    """
    Represents a single statement (triple) in the graph.
    Immutable by design - modifications are made by adding new statements.
    """
    id: str  # UUID for the statement
    subject: EntityId
    predicate: EntityId  # Must be a property type
    object: Union[EntityId, str]  # Can be either an entity or a literal value
    timestamp: datetime
    node_id: str  # ID of the node that created this statement
    certainty: float = 1.0  # Confidence in the statement's truth (0.0 to 1.0)
    
    def __post_init__(self):
        if self.predicate.id_type != EntityType.PROPERTY:
            raise ValueError("Predicate must be a property type entity")

class GraphLayer:
    """
    Core graph storage and manipulation layer.
    Maintains CRDT sets of entities and statements.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.entities: Dict[EntityId, Entity] = {}
        self.statements: Set[Statement] = set()
        self._local_id_counter = 0
    
    def create_entity(self, entity_type: EntityType = EntityType.STANDARD) -> Entity:
        """Creates a new entity with a unique ID."""
        self._local_id_counter += 1
        entity_id = EntityId(
            id_type=entity_type,
            local_id=str(self._local_id_counter),
            node_id=self.node_id
        )
        entity = Entity(
            id=entity_id,
            created_at=datetime.now()
        )
        self.entities[entity_id] = entity
        return entity
    
    def add_label(self, entity_id: EntityId, label: str, language: str = "en") -> None:
        """Adds a label to an entity in a specific language."""
        entity = self.entities.get(entity_id)
        if not entity:
            raise ValueError(f"Entity {entity_id} not found")
        
        if language not in entity.labels:
            entity.labels[language] = set()
            
        # Add to the CRDT set with timestamp and node_id
        entity.labels[language].add((label, datetime.now(), self.node_id))
    
    def add_statement(self, subject: EntityId, predicate: EntityId, 
                     object_: Union[EntityId, str], certainty: float = 1.0) -> Statement:
        """Adds a new statement to the graph."""
        statement = Statement(
            id=str(uuid.uuid4()),
            subject=subject,
            predicate=predicate,
            object=object_,
            timestamp=datetime.now(),
            node_id=self.node_id,
            certainty=certainty
        )
        self.statements.add(statement)
        return statement
    
    def get_latest_label(self, entity_id: EntityId, language: str = "en") -> Optional[str]:
        """Gets the most recent label for an entity in a specific language."""
        entity = self.entities.get(entity_id)
        if not entity or language not in entity.labels:
            return None
            
        # Get the label with the latest timestamp
        latest = max(entity.labels[language], key=lambda x: x[1])
        return latest[0]
    
    def merge(self, other_graph: 'GraphLayer') -> None:
        """
        Merges another graph into this one.
        Implements CRDT merge operation.
        """
        # Merge entities
        for entity_id, entity in other_graph.entities.items():
            if entity_id not in self.entities:
                self.entities[entity_id] = entity
            else:
                # Merge labels and descriptions (CRDT union)
                for lang, labels in entity.labels.items():
                    if lang not in self.entities[entity_id].labels:
                        self.entities[entity_id].labels[lang] = set()
                    self.entities[entity_id].labels[lang].update(labels)
                
                for lang, descs in entity.descriptions.items():
                    if lang not in self.entities[entity_id].descriptions:
                        self.entities[entity_id].descriptions[lang] = set()
                    self.entities[entity_id].descriptions[lang].update(descs)
        
        # Merge statements (CRDT union)
        self.statements.update(other_graph.statements)

    def query(self) -> 'GraphQuery':
        """
        Creates a new query builder instance for this graph.
        This method connects the GraphQuery system to our GraphLayer.
        """
        from graph_query_system import GraphQuery  # Import here to avoid circular imports
        return GraphQuery(self)

