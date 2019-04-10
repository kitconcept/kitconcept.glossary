import GlossaryTip from './js/glossarytip.js';


// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];


$(() => {
  if ($('.highlightedGlossaryTerm').length > 0) {
    new GlossaryTip();
  }
});


export default {
  GlossaryTip,
}
