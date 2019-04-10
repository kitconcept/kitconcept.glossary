import tippy from 'tippy.js';


export default class GlossaryTip {
  constructor() {
    this.$template = $('<div>');

    // Change this option when style the tooltip
    this.dontHide = false;

    this.createTooltip();
    $('.highlightedGlossaryTerm').on('click', this.onClick.bind(this));
  }
  createTooltip() {
    tippy('.highlightedGlossaryTerm', {
      animation: 'shift-toward',
      arrow: true,
      theme: 'light',
      placement: 'bottom',
      html: this.$template[0],
      onShow: this.onShow.bind(this),
      // prevent tooltip from displaying over button
      popperOptions: {
        modifiers: {
          preventOverflow: {
            enabled: false
          },
          hide: {
            enabled: false
          }
        }
      }
    });
  }
  onShow(tip) {
    if (this.dontHide) {
      tip.hide = function() {};
    }

    let $tip = $(tip.reference);
    let $popup = $('.tippy-content', tip.popper);

    $popup.html(`
      <div class="glossary-definition-popup">
        <h6 class="glossary-term">
          ${$tip.attr('data-term')}
        </h6>
        <div class="glossary-definition">
          ${$tip.attr('data-definition')}
        </div>
      </div>
    `);
  }
  onClick(e) {
    e.preventDefault();
    let $tip = $(e.target);
    location.href = $tip.attr('data-url');
  }
}
