import GlossaryTip from "./js/glossarytip.js";
import GlossaryMarker from "./js/glossarymarker.js";

// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];

$(() => {
  function setHeader(xhr) {
    xhr.setRequestHeader("Accept", "application/json");
  }
  var body = jQuery("body");
  var portalURL = body.data('portal-url');

  // get portal type
  var bodyClass = body.attr('class');
  var matches = /portaltype-([^ ]*) /.exec(bodyClass);
  var portalType = matches ? matches[1] : '';
  console.log(portalType);

  jQuery.ajax({
    url: portalURL + "/@glossary_terms",
    dataType: "json",
    success: data => {
      console.log(data);
      var enabledTypes = [];
      jQuery.each(data.settings.enabled_types, function(index, name) {
        enabledTypes.push(name.toLowerCase().replace(' ', '-'));
      });
      console.log(enabledTypes);

      // The GlossaryMarker code removes marker text from edit forms
      if ($(".template-edit").length > 0) {
        return;
      }

      if (!data.settings.enabled ||
          enabledTypes.indexOf(portalType) === -1) {
        console.log('not enabled (globally or for this type)');
        return;
      }
      var gm = new GlossaryMarker(data.terms);
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
