import GlossaryTip from "./js/glossarytip.js";
import GlossaryMarker from "./js/glossarymarker.js";

// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];

$(() => {
  function setHeader(xhr) {
    xhr.setRequestHeader("Accept", "application/json");
  }
  var portalURL = jQuery("body").data('portal-url');
  jQuery.ajax({
    url: portalURL + "/@glossary_terms",
    dataType: "json",
    success: data => {
      var gm = new GlossaryMarker(data);
      console.log(data);
      var target_node = document.getElementById("content");
      gm.highlight_related_glossary_terms_in_node(
        target_node,
        gm.unauthorized_tags
      );
      if ($(".highlightedGlossaryTerm").length > 0) {
        new GlossaryTip();
      }
    },
    beforeSend: setHeader
  });
});

export default {
  GlossaryTip
};
