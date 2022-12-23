jQuery.validator.addMethod("label", function (value, element) {
    return this.optional(element) || /^[\w\s\(\)\.\-\$#]+$/i.test(value);
}, "Labels may only contain letters, numbers, spaces, and these characters: ( ) . - # $");

let getRootElement = function (el, selector) {
    el = $(el)
    if (!el.is(selector))
        el = el.parents(selector)
    return el
}
