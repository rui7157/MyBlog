Freeze the state of data-structures and objects for data-analysis or testing
(diffing data-structures). Frozen data-structures consist of only tuples
and these are comparable/sortable/hashable. The freeze() function can be used
for many purposes for example implement __hash__() for your complex object
very fast. dump() is intended for testing and analysis.

