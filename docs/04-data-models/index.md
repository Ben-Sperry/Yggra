# 4. Data Models

## 4.1 Core Data Structures

At the heart of Yggra lies a carefully designed set of data structures that enable flexible data representation while maintaining strict consistency guarantees. These structures build upon each other to create a complete system for representing personal information.

The foundational principle is that all information in the system can be decomposed into atomic statements about entities. These statements, when combined with the property model and storage references, create a complete and flexible system for representing any type of personal data.

Each data structure includes mandatory metadata that enables tracking of provenance, timing, and authorization throughout the system. This metadata is crucial for maintaining security and enabling controlled sharing of information.

## 4.2 Entity-Property Model

The entity-property model defines how information is represented in the graph layer. Unlike traditional database systems where entities have fixed schemas, Yggra entities are defined by their relationships and properties, allowing for flexible and evolving representations.

An entity is formally defined as:

```python
class Entity:
    id: UUID            # Globally unique identifier
    created_at: datetime # Creation timestamp
    node_id: str        # ID of creating node
    metadata: Dict      # System-level metadata
    
    # CRDT sets for multilingual support
    labels: Dict[str, Set[Tuple[str, datetime, str]]]
    descriptions: Dict[str, Set[Tuple[str, datetime, str]]]
```

Properties are themselves entities, but with special handling:

```python
class Property(Entity):
    domain: Set[Type]    # Valid subject types
    range: Set[Type]     # Valid object types
    cardinality: str     # one|many
    symmetrical: bool    # If true, relationship goes both ways
    transitive: bool     # If true, relationship chains are valid
```

This model enables several powerful features:
- Flexible entity definitions that can evolve over time
- Strong typing through property constraints
- Multi-language support through CRDT label sets
- System-level metadata separation from entity data

## 4.3 Statement Model

Statements are the atomic units of information in the system. Each statement represents a single fact about an entity and is immutable once created. This immutability is key to maintaining consistency and enabling distributed operation.

A statement is formally defined as:

```python
class Statement:
    id: UUID             # Unique statement identifier
    subject: UUID        # Entity this statement is about
    predicate: UUID      # Property being defined
    object: Any          # Value or reference to another entity
    timestamp: datetime  # When the statement was created
    creator_node: str    # ID of creating node
    certainty: float     # Confidence level (0.0-1.0)
    provenance: Dict     # Origin information
    
    # For distributed operation
    vector_clock: Dict[str, int]  # Causal ordering
    signature: bytes              # Creator's signature
```

The statement model ensures:
- Complete history preservation
- Clear provenance tracking
- Cryptographic verification
- Distributed consistency
- Temporal ordering

## 4.4 Application View Model

Application views provide a bridge between the graph's statement-based model and application-specific data structures. A view definition includes both the structure of the expected data and rules for translating between graph and application representations.

```python
class ViewSchema:
    name: str                    # Unique view identifier
    version: str                 # Schema version
    structure: Dict             # Expected data structure
    property_mappings: Dict     # Graph to app field mappings
    constraints: List[Rule]     # Data validation rules
    update_policy: UpdatePolicy # How changes are handled
    cache_policy: CachePolicy  # View maintenance rules
```

View schemas support:
- Multiple versions of the same basic structure
- Flexible property mapping
- Constraint validation
- Update and cache policy specification

## 4.5 Storage Reference Model

Storage references create an abstraction layer between the graph layer and physical storage. They contain all information needed to locate and validate stored data without exposing storage implementation details.

```python
class StorageReference:
    id: UUID                # Reference identifier
    content_hash: str       # Data integrity hash
    size: int              # Content size in bytes
    mime_type: str         # Content type
    encryption_info: Dict  # Encryption metadata
    location: Dict         # Backend-specific location info
    
    # Performance optimization
    access_pattern: Dict   # Usage statistics
    replicas: List[str]    # Replica locations
    
    # Security
    access_control: Dict   # Permission information
    audit_log: List       # Access history
```

This model enables:
- Location-independent data access
- Transparent encryption
- Integrity verification
- Access control at the storage level
- Performance optimization through replication

The storage reference model is particularly important as it allows the system to optimize data placement and access patterns without requiring changes to the graph layer or application interfaces. Combined with intelligent storage management policies, this enables efficient handling of both small metadata and large binary objects while maintaining a consistent interface for all data types.