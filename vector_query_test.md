# Vector Query Test

## Query

**"Is physical therapy covered under the Silver plan?"**

The query was first run without any metadata filter and then repeated with a `plan_type` filter for the Silver plan.

## Unfiltered Query

The unfiltered query returned one result:

* **ID:** `benefits_1`
* **Plan:** Gold PPO
* **Section:** coverage
* **Distance:** `1.0958092212677002`

The returned document contains the Gold PPO sample Summary of Benefits and Coverage.

## Metadata-Filtered Query

The same query was executed with:

```python
where={"plan_type": "Silver"}
```

The filtered query returned **zero results**.

## Result

The metadata filter successfully scoped the search to documents whose `plan_type` is `"Silver"`. Since the returned document from the unfiltered search has `plan_type: "Gold PPO"`, it was excluded from the filtered query.

This confirms that Chroma's metadata filtering works as expected and prevents results from other plans from being returned when a specific plan is requested.
