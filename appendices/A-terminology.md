# Appendix A: Terminology

## Core Concepts

### Entity
The fundamental unit of information in Yggra. Unlike traditional database records, entities are defined by their properties and relationships rather than by fixed schemas. An entity can represent anything from a digital file to an abstract concept. Entities are identified by globally unique identifiers but are primarily understood through their characteristics and relationships to other entities.

### Statement
An immutable assertion about an entity, expressed as a triple of (subject, predicate, object). Statements are the atomic units of truth in the system. They can never be modified or deleted, only superseded by new statements. This immutability is key to maintaining consistency and enabling distributed operation.

### Property
A special type of entity that defines a kind of relationship or characteristic. Properties are similar to predicates in logic or columns in a database, but they are more flexible as they can be created and evolved dynamically. Properties themselves can have properties, enabling rich metadata about relationships.

### Graph
The complete collection of entities and statements that represent a user's personal information space. Unlike traditional graphs, the Yggra graph is immutable and append-only. Each user maintains their own sovereign graph, though they may share facets of it with others.

## Data Access Concepts

### Facet
A dynamic, bi-directional interface that gives meaning to graph data for specific purposes. Like a facet of a gemstone both receives and reflects light, a facet in Yggra both presents data in application-specific ways and allows modifications through that same structure. Facets can manifest as familiar data structures (SQL databases, file systems, document stores) while maintaining the integrity of the underlying graph.

Key characteristics of facets include:
- Transformation: Each facet presents data in a way that makes sense for its specific purpose
- Bi-directionality: Changes made through a facet propagate back to the graph
- Privacy-awareness: Facets automatically apply appropriate privacy transformations
- Structure-independence: The same underlying data can be presented through multiple facets
- Semantic preservation: Relationships and meaning are maintained across different facets

### Data Structure Interpreter
A component that translates between graph statements and specific facet manifestations. Interpreters enable applications to work with familiar data structures while leveraging the graph's capabilities. They handle both reading from and writing to the graph through the facet's interface.

### Query
A request for information from the graph, potentially through one or more facets. Queries in Yggra are more sophisticated than traditional database queries as they can traverse relationships, apply privacy transformations, and respect sharing boundaries automatically.

## Sharing Concepts

### Shared Facet
A specialized facet created for sharing data with other users. Unlike traditional sharing mechanisms, shared facets are dynamic, revocable, and can apply sophisticated privacy transformations. They enable fine-grained control over what information is shared and how it can be accessed while maintaining the natural structure of the data for the recipient.

### Facet Composition
The process of combining multiple facets to create new perspectives on data. This enables applications to work with data from multiple sources while maintaining appropriate boundaries and transformations for each source.

[Previous Storage Concepts, Privacy and Security Concepts, System Concepts remain largely unchanged]

## Additional Terms

### Faceted Identity
The concept that entities can present different aspects of themselves through different facets while maintaining a coherent underlying identity in the graph. This enables flexible and context-appropriate presentation of information while maintaining data sovereignty.

### Semantic Crystallization
The process by which raw graph data takes on specific meaning and structure through facets, similar to how crystalline structures give form to raw materials. This process is reversible and can happen in multiple ways through different facets.

### Facet Evolution
The process by which facets adapt to changing application needs without requiring changes to the underlying graph structure. Because the graph stores atomic statements rather than structured data, facets can evolve independently of the data they present.