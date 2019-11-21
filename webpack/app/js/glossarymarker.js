/* Add markup to highlight the glossry terms in content. Mostly a direct
port from Products.PloneGlossary */

//
// Dig into all glossary definition
//

export default class GlossaryMarker {
  constructor(terms) {
    this.terms = terms;
    this.dictionary_found = [];
    this.CBrowser = this.CBrowser.bind({});
    this.browserInfo = this.CBrowser();
    this.unauthorized_tags = ["a"];
  }

  debug() {
    debugger;
  }

  CBrowser() {
    var ua, s, i;
    var info = {};
    info.isIE = false; // Internet Explorer
    info.isNS = false; // Netscape
    info.isOP = false; // Opera
    info.version = null;

    ua = navigator.userAgent;

    s = "Opera";
    if ((i = ua.indexOf(s)) >= 0) {
      info.isOP = true;
      info.version = 7;
      return info;
    }

    s = "MSIE";
    if ((i = ua.indexOf(s)) >= 0) {
      info.isIE = true;
      info.version = parseFloat(ua.substr(i + s.length));
      return info;
    }
    s = "Netscape6/";
    if ((i = ua.indexOf(s)) >= 0) {
      info.isNS = true;
      info.version = parseFloat(ua.substr(i + s.length));
      return info;
    }

    // Treat any other "Gecko" browser as NS 6.1.

    s = "Gecko";
    if ((i = ua.indexOf(s)) >= 0) {
      info.isNS = true;
      info.version = 6.1;
      return info;
    }
    return info;
  }

  highlight_related_glossary_term_in_text(node, word, definition_index) {
    var class_name = "highlightedGlossaryTerm";
    var parent_node = node.parentNode;
    //glossary inserted node, don't process
    if (parent_node.className == class_name) {
      return;
    }

    var lword = word.toLowerCase();
    // Only highlight the first instance found ?
    if (typeof this.dictionary_found != "undefined") {
      if (this.dictionary_found[lword] === "1") {
        return;
      }
    }
    var content_value = node.nodeValue;
    var lcontent_value = content_value.toLowerCase();
    console.log('============================================================');
    console.log(lcontent_value);
    var word_bounds = new Array();
    /* Write multiple regexps to replace one because it doesn't work
     * on IE: '\\b' + lword + '\\b'

     * Please keep this in the order that finds the first match first:
     * in a sentence with 'word word' the first word should be found
     * first, so its regexp needs to be listed before the regexp that
     * only finds words mid-sentence. */
    word_bounds.push("^" + lword + "$"); // word is the sentence
    word_bounds.push("^" + lword + "\\W"); // word is beginning a sentence
    // Note: for the next two, the found index includes the blank
    // space, so we need to increase the index when we loop over it.
    word_bounds.push("\\W" + lword + "\\W"); // word is included in a sentence
    word_bounds.push("\\W" + lword + "$"); // word is finishing a sentence
    var index = -1;

    // Check each regexps
    for (var i = 0; i < word_bounds.length; i++) {
      index = lcontent_value.search(word_bounds[i]);
      console.log(word_bounds[i]);
      console.log(index);
      if (index != -1) {
        if (i == 2 || i == 3) {
          // Position of search is one character before the real
          // start of the word.  See the note above.
          index += 1;
        }
        break;
      }
    }
    if (index == -1) {
      console.log('======== not found =========');
      return;
    }
    console.log('======== found =========');

    // Word is found
    var last_index = index + word.length;

    // Only highlight the first instance found ?
    if (typeof this.dictionary_found != "undefined") {
      this.dictionary_found[lword] = "1";
    }

    if (index != -1) {
      // Create Highlighted term
      var hiword = document.createElement("span");
      hiword.className = class_name;
      hiword.appendChild(
        document.createTextNode(content_value.substr(index, word.length))
      );

      // Add popup events
      var term = this.terms[definition_index];
      hiword.setAttribute("data-term", term.title);
      hiword.setAttribute("data-definition", "fixme");
      hiword.setAttribute("data-url", term.url);
      hiword.setAttribute("data-definition", term.definition);

      parent_node.insertBefore(
        document.createTextNode(content_value.substr(0, index)),
        node
      );
      parent_node.insertBefore(hiword, node);
      parent_node.insertBefore(
        document.createTextNode(content_value.substr(index + word.length)),
        node
      );
      parent_node.removeChild(node);
    }
  }
  highlight_related_glossary_term_in_node(
    node,
    word,
    definition_index,
    unauthorized_tags
  ) {
    // Traverse childnodes
    if (!node) {
      return false;
    }

    // Don't dig into unauthorized keys
    var tag_name = node.nodeName.toLowerCase();

    var tag_id = node.id;
    var tag_class = node.className;

    for (i = 0; i < unauthorized_tags.length; i++) {
      var unauthorized_tag_name = unauthorized_tags[i].toLowerCase();
      if (
        tag_name == unauthorized_tag_name ||
        tag_name + "#" + tag_id == unauthorized_tag_name ||
        tag_name + "." + tag_class == unauthorized_tag_name
      ) {
        return false;
      }
    }

    if (node.hasChildNodes) {
      var i;
      for (i = 0; i < node.childNodes.length; i++) {
        this.highlight_related_glossary_term_in_node(
          node.childNodes[i],
          word,
          definition_index,
          unauthorized_tags
        );
      }

      if (node.nodeType == 3) {
        // Check all textnodes.
        this.highlight_related_glossary_term_in_text(
          node,
          word,
          definition_index
        );
      }
    }
    return true;
  }

  highlight_related_glossary_terms_in_node(target_node, unauthorized_tags) {
    // Init terms in definition node
    for (var def_index = 0; def_index < this.terms.length; def_index++) {
      var terms = this.terms[def_index]["terms"];
      for (var term_index = 0; term_index < terms.length; term_index++) {
        var word = terms[term_index];
        this.highlight_related_glossary_term_in_node(
          target_node,
          word,
          def_index,
          unauthorized_tags
        );
      }
    }
  }
}

function build_related_glossary_terms_list(target_node) {
  // Build list of related terms
  if (this.terms.length > 0) {
    var i = 0;
    var ul_node = document.createElement("ul");

    // create li node
    for (i = 0; i < this.terms.length; i++) {
      if (this.terms[i]["show"] == "1") {
        var li_node = document.createElement("li");

        // Add link tag
        var a_node = document.createElement("a");
        var url = this.terms[i]["url"];
        a_node.setAttribute("href", url);
        var title_text = this.terms[i]["title"];
        a_node.appendChild(document.createTextNode(title_text));

        li_node.appendChild(a_node);
        ul_node.appendChild(li_node);
      }
    }

    target_node.appendChild(ul_node);
  }
}
