from typing import List, Set, Dict, Any, Optional, Callable, TypeVar, Generic, Union
from dataclasses import dataclass
from enum import Enum
from graph_layer_core import GraphLayer, EntityId, Statement

T = TypeVar('T')

class QueryResultType(Enum):
    """Defines what kind of results a query should return"""
    ENTITIES = "entities"
    STATEMENTS = "statements"
    VALUES = "values"
    PATHS = "paths"

@dataclass
class QueryResult(Generic[T]):
    """
    Container for query results that includes metadata about the query execution
    and maintains deterministic ordering.
    """
    results: List[T]
    total_matches: int
    execution_time_ms: float
    
    def __iter__(self):
        return iter(self.results)

class GraphQuery:
    """
    Query builder for the graph layer. Provides a fluent interface for constructing
    complex queries that will be executed by applications.
    """
    def __init__(self, graph: GraphLayer):
        self.graph = graph
        self.start_entities: Set[EntityId] = set()
        self.property_chains: List[List[EntityId]] = []
        self.filters: List[Callable] = []
        self.result_type = QueryResultType.ENTITIES
        self.limit: Optional[int] = None
        self.offset: Optional[int] = None
        self._order_by: List[Callable] = []
        
    def starting_from(self, entity_ids: Union[EntityId, List[EntityId]]) -> 'GraphQuery':
        """Define the starting point(s) for the query."""
        if isinstance(entity_ids, EntityId):
            self.start_entities.add(entity_ids)
        else:
            self.start_entities.update(entity_ids)
        return self
    
    def follow(self, property_id: EntityId) -> 'GraphQuery':
        """Add a property to follow in the graph traversal."""
        self.property_chains.append([property_id])
        return self
    
    def follow_chain(self, property_ids: List[EntityId]) -> 'GraphQuery':
        """Follow a chain of properties in sequence."""
        self.property_chains.append(property_ids)
        return self
        
    def filter(self, predicate: Callable) -> 'GraphQuery':
        """Add a filter function to the query."""
        self.filters.append(predicate)
        return self
    
    def order_by(self, key_func: Callable) -> 'GraphQuery':
        """Define sort order for results."""
        self._order_by.append(key_func)
        return self
    
    def limit(self, n: int) -> 'GraphQuery':
        """Limit the number of results returned."""
        self.limit = n
        return self
    
    def offset(self, n: int) -> 'GraphQuery':
        """Skip the first n results."""
        self.offset = n
        return self
    
    def return_entities(self) -> 'GraphQuery':
        """Set query to return matched entities."""
        self.result_type = QueryResultType.ENTITIES
        return self
    
    def return_statements(self) -> 'GraphQuery':
        """Set query to return matched statements."""
        self.result_type = QueryResultType.STATEMENTS
        return self
    
    def return_values(self) -> 'GraphQuery':
        """Set query to return literal values."""
        self.result_type = QueryResultType.VALUES
        return self
    
    def return_paths(self) -> 'GraphQuery':
        """Set query to return entire paths that matched."""
        self.result_type = QueryResultType.PATHS
        return self

    def execute(self) -> QueryResult:
        """
        Execute the query and return results.
        The execution follows these steps:
        1. Start with the initial entities
        2. For each property chain, follow the relationships
        3. Apply filters at each step
        4. Transform results based on return type
        5. Apply sorting and pagination
        """
        import time
        start_time = time.perf_counter_ns()  # Using nanosecond precision
        
        # Start with our initial entity set
        current_entities = self.start_entities
        
        # Follow each property chain
        for chain in self.property_chains:
            next_entities = set()
            for entity_id in current_entities:
                # Find statements matching the current entity and property
                for statement in self.graph.statements:
                    if statement.subject == entity_id and statement.predicate == chain[0]:
                        if isinstance(statement.object, EntityId):
                            next_entities.add(statement.object)
            current_entities = next_entities
        
        # Apply filters
        filtered_entities = set()
        for entity_id in current_entities:
            entity = self.graph.entities.get(entity_id)
            if entity and all(f(entity) for f in self.filters):
                filtered_entities.add(entity_id)
        
        # Transform results based on return type
        if self.result_type == QueryResultType.ENTITIES:
            results = [self.graph.entities[eid] for eid in filtered_entities]
        elif self.result_type == QueryResultType.STATEMENTS:
            results = [s for s in self.graph.statements 
                      if s.subject in filtered_entities]
        elif self.result_type == QueryResultType.VALUES:
            results = [self.graph.get_latest_label(eid) for eid in filtered_entities]
        else:  # PATHS
            results = []  # Path finding to be implemented
        
        # Apply sorting
        for key_func in reversed(self._order_by):
            results.sort(key=key_func)
        
        # Apply pagination
        if self.offset:
            results = results[self.offset:]
        if self.limit:
            results = results[:self.limit]
        
        execution_time = (time.perf_counter_ns() - start_time) / 1_000_000  # Convert nanoseconds to milliseconds
        
        return QueryResult(
            results=results,
            total_matches=len(filtered_entities),
            execution_time_ms=execution_time
        )