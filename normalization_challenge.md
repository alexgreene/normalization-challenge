Three different sellers have tickets for a baseball game...

```
quantity: 2,
price: 50,
section: "133",
row: "C"
```

```
quantity: 4
price: 55
section: "S133",
row : "b"
```

```
quantity: 1,
price: 45,
section: "Field Level 133",
row: "Row C"
```

Each has a different representation of the same tickets. The challenge is to map each of the tickets given to us by a seller to the correct ticket from a manifest of ticket sections at the stadium. You cannot trust that sellers will even have a section/row spelled correctly or even in the ballpark (no pun intended) of the correct name.

## Your Task

The task is to implement a section normalizer that works on two venues with a high degree of accuracy. You will do this by implementing two stub methods in the provided file (`normalizer.py`).

## Manifest Data

| section_id | section_name     | row_id | row_name |
|------------|------------------|--------|----------|
| 1          | 133              | 0      | A        |
| 1          | 133              | 2      | C        |
| 1          | 133              | 1      | B        |
| 1          | 133              | 4      | E        |
| 1          | 133              | 3      | D        |
| 215        | 432              | 0      | 1        |
| 215        | 432              | 2      | 3        |
| 215        | 432              | 1      | 2        |
| 215        | 432              | 4      | 5        |
| 215        | 432              | 3      | 4        |
| 216        | Empire Suite 241 |        |          |

As you can see, each distinct section has an identifier `section_id`; what we'd like to do is match a listing to a `(section_id, row_id)` so we can render it on our map, or decide whether the listing is 'garbage' and hide it from our customers.

## Training Data

You are provided with two input datasets. Each dataset is a CSV file with the following format

| section           | row | n_section_id | n_row_id | valid |
|-------------------|-----|--------------|----------|-------|
| Section 432       | 1   | 215          | 0        | TRUE  |
| Section 432       | 2   | 215          | 1        | TRUE  |
| Section 432       | 99  | 215          |          | FALSE |
| Promenade Box 432 | 1   | 215          | 0        | TRUE  |
| sdlkjsdflksjdf    | 1   |              |          | FALSE |
| 432               | 1-5 | 215          |          | FALSE |


