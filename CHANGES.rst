Changelog
=========


1.0.0a7 (2019-11-22)
--------------------

- Don't run the highlighter on edit forms as it will remove the term
  text from form fields.
  [csenger]

- Fix the templates to run in that don't have ATContentTypes.
  [csenger]

- Use an unminified build with debug output for now.
  [csenger]

- Fix German translation for Glossary description.
  [timo, csenger]


1.0.0a6 (2019-11-11)
--------------------

- Update German translations.
  [timo]

1.0.0a5 (2019-11-08)
--------------------

- Black.
  [timo]


1.0.0a4 (2019-11-08)
--------------------

- Use Portal Transforms transformation to generate glossary entries.
  [csenger]

- Show definition in list view with configurable truncation.
  [csenger]

- Rename 'Term' to 'GlossaryTerm'.
  [timo]

- Add 'Glossary' type to displayed_types that show up in the navigation.
  [timo]


1.0.0a3 (2019-05-28)
--------------------

- The default exclude_from_navigation behavior always return default value
  as False, and the adapter supposed to give tha hability to change
  the default value to True is broken.
  The behavior is being override here with defaut value as True to always
  exclude from navigation the Term items (same behavior as
  Producst.PloneGlossary).
  [rodfersou]


1.0.0a2 (2019-05-27)
--------------------

- Add support for Archetypes.
  [rodfersou]


1.0.0a1 (2019-05-09)
--------------------

- Initial release.
  [kitconcept]
