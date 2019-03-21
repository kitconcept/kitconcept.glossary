const makeConfig = require('sc-recipe-staticresources');


module.exports = makeConfig(
  //name
  'kitconcept.glossary',

  //shortName
  'glossary',

  //path
  `${__dirname}/../src/kitconcept/glossary/browser/static`,

  //publicPath
  '++resource++kitconcept.glossary/',

  //callback
  (config, options) => {
    config.entry.unshift(
      './app/img/glossary-icon.png',
      './app/img/term-icon.png',
    );
  },
);
