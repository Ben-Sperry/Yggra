# 2. Architectural Overview

## 2.1 System Architecture

Yggra employs a three-layer architecture where each layer serves a distinct purpose in managing personal data. A key architectural principle is that while applications and storage systems may be shared across users, each individual maintains their own private graph layer that serves as their personal knowledge base.

### Three-Layer Design

#### Application Interface Layer (Top)
The application interface layer provides standardized ways for applications to interact with personal data. While many users might use the same application (like a social media client or photo management tool), each instance of the application interacts with that specific user's personal graph through interfaces tailored to the application's needs. This layer handles:
- Translation between application data structures and graph semantics
- Schema mapping and validation
- View generation and maintenance
- Access control and sharing management
- Cache management

Applications themselves can be shared and standardized across users, but their data interactions are always mediated through the individual user's personal graph.

#### Graph Layer (Middle)
The graph layer is the heart of personal data sovereignty in Yggra. Each user maintains their own private graph that serves as the authoritative source of truth for all their personal information. This layer is:
- Unique to each individual user
- Completely private and secure
- Controlled solely by the user
- Independent of other users' graphs

The graph layer manages:
- Entity relationships and properties specific to the user
- Immutable statements about personal data
- Query processing within the personal graph
- CRDT-based consistency for personal data
- Graph integrity and validation

While users may share views into their graph data, they never share direct access to the graph itself. This ensures that each user maintains complete control over their personal information while still enabling rich data sharing capabilities through controlled interfaces.

#### Storage Layer (Bottom)
The storage layer manages the physical storage of data across various backends, potentially sharing storage infrastructure while maintaining data privacy. It can:
- Use shared storage systems like IPFS for efficient data deduplication
- Maintain private encrypted storage for sensitive data
- Optimize storage placement across different backends
- Handle backup and replication strategies
- Manage encryption at rest

While the storage layer might leverage shared infrastructure (like IPFS) for efficiency, it maintains strict separation between users' data through encryption and access controls.

### Component Interactions

Data flows through the system while maintaining personal boundaries:

Ingestion Path:
1. Applications submit data through their interface
2. Interface layer decomposes data into statements for the user's personal graph
3. The user's graph layer records statements and relationships
4. Storage layer handles physical data placement with appropriate privacy controls

Sharing Path:
1. User creates a controlled view of specific graph data
2. System generates secure access credentials for the view
3. Other users' applications can access shared data through the view
4. Original user maintains control and can revoke access

This architecture ensures that while users can share data efficiently, they never lose control over their personal information. The graph layer acts as a secure personal foundation that mediates all data access and sharing, while leveraging shared infrastructure at the storage and application layers for efficiency.

### System Boundaries

The system operates within clear boundaries:

- External: Applications interact only through the interface layer
- Internal: Each layer communicates only with adjacent layers
- Physical: Storage backends are accessed only through the storage layer

## 2.2 Design Philosophy

The architecture embodies several key philosophical principles:

### Separation of Concerns
Each layer has a single, well-defined responsibility. This separation allows components to evolve independently and optimizes each layer for its specific purpose.

### Information Hiding
Implementation details of each layer are hidden from the others. Applications need not understand graph structure, and the graph layer need not understand storage mechanisms.

### Data Independence
Applications are isolated from both the logical structure (graph) and physical storage of data. This independence allows the system to evolve without requiring application changes.

### Progressive Enhancement
The system can operate at different levels of sophistication:
- Basic: Simple file storage and retrieval
- Standard: Semantic data organization and querying
- Advanced: Complex relationship analysis and inference

## 2.3 Key Design Decisions

### Immutable Graph Structure
The decision to make all graph operations additive rather than modifying ensures:
- Simplified consistency model
- Complete data history
- Easier distributed operation
- Natural support for versioning

### Interface Layer Flexibility
Supporting multiple data structure interpreters allows:
- Easier adoption by existing applications
- Support for various programming paradigms
- Progressive migration paths
- Optimized access patterns

### Storage Layer Abstraction
Abstracting storage operations enables:
- Optimal data placement
- Transparent encryption
- Efficient resource utilization
- Future storage technology adoption

## 2.4 Architectural Constraints

The architecture operates under several constraints:

### Consistency Requirements
- Graph operations must be atomic
- Statement order must be preserved
- Entity relationships must remain valid

### Performance Boundaries
- View generation must be efficient enough for interactive use
- Query response times must meet application needs
- Storage operations must handle large data volumes

### Security Constraints
- Access control must be enforced at all layers
- Data privacy must be maintained during sharing
- Storage encryption must be transparent

### Resource Limitations
- Memory usage must scale with active dataset size
- Storage capacity must be managed across backends
- Network bandwidth must be used efficiently
