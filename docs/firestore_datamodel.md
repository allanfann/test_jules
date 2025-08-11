# Firestore Data Model for Decision Trees

This document outlines the data structure used to store and manage decision trees in Google Firestore.

## Data Structure Overview

We use a hierarchical data model where each decision tree is a document in a top-level collection, and the nodes of that tree are stored in a sub-collection.

-   **Top-level Collection:** `decision_trees`
-   **Document:** `/{tree_id}` (e.g., `get-married`)
-   **Sub-collection:** `/{tree_id}/nodes`
-   **Node Document:** `/{node_id}` (e.g., `node_01`)

---

## 1. `decision_trees` Collection

This collection contains a document for each decision tree available in the system.

### Document Fields (`/{tree_id}`)

-   **`name`** (String): The human-readable name of the decision tree.
    -   *Example:* "是否要與眼前的伴侶結婚"
-   **`description`** (String): A brief description of what the tree helps to decide.
    -   *Example:* "A decision tree to help evaluate the complex decision of getting married."
-   **`root_node_id`** (String): The ID of the root node for this tree. This is the starting point for any traversal.
    -   *Example:* "node_01"

### Example `decision_trees` Document

**Path:** `/decision_trees/get-married`

```json
{
  "name": "是否要與眼前的伴侶結婚",
  "description": "A decision tree to help evaluate the complex decision of getting married.",
  "root_node_id": "node_01"
}
```

---

## 2. `nodes` Sub-collection

This sub-collection exists within each `decision_tree` document and contains all the nodes for that specific tree.

### Document Fields (`/{tree_id}/nodes/{node_id}`)

-   **`type`** (String): The type of node. This can be one of two values:
    -   `'DECISION'`: Represents a question or a decision point in the tree.
    -   `'OUTCOME'`: Represents a terminal node or a final answer/conclusion.
-   **`text`** (String): The content of the node.
    -   If `type` is `DECISION`, this is the question to be asked (e.g., "價值觀契合?").
    -   If `type` is `OUTCOME`, this is the final result (e.g., "結婚").
-   **`children`** (Array of Maps): This field only exists for nodes of `type: 'DECISION'`. It is an array where each item represents a possible answer and the path to the next node.
    -   **`answer_text`** (String): The text for the answer/branch (e.g., "是" or "否").
    -   **`next_node_id`** (String): The ID of the node to traverse to if this answer is chosen.

### Example `nodes` Documents

**Path:** `/decision_trees/get-married/nodes/node_01` (A decision node)

```json
{
  "type": "DECISION",
  "text": "價值觀契合?",
  "children": [
    { "answer_text": "是", "next_node_id": "node_02" },
    { "answer_text": "否", "next_node_id": "outcome_01" }
  ]
}
```

**Path:** `/decision_trees/get-married/nodes/outcome_01` (An outcome node)

```json
{
  "type": "OUTCOME",
  "text": "不結婚"
}
```
