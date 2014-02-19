Indexer Test Set
================

The following tests are to validate indexer's behavior.

Rapp to Rapp
---

*Basic*

:: 
  Child -> Parent

*Chained*

::
  Child -> Parent -> Grandma

*Multiple Child*

::
  Child1 ->
            Parent
  Child2 ->

*Cyclic*

::
  Child -> Parent -> Child

*Malformed Parent*

::
  Child -> Malformed Parent


Meta Rapp
---

*Basic*

:: 
  Child -> Meta Rapp

*Malformed Meta Rapp*

::
  Child -> Malformed Meta Rapp
