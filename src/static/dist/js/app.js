jQuery.validator.addMethod("label", function (value, element) {
    return this.optional(element) || /^[\w\s\(\)\.\-\$#]+$/i.test(value);
}, "Labels may only contain letters, numbers, spaces, and these characters: ( ) . - # $");

jQuery.validator.addMethod("zipcode", function (value, element) {
    return this.optional(element) || /^\d{5}(?:-\d{4})?$/.test(value);
}, "Please provide a valid zipcode.");

jQuery.validator.addMethod("macaddress", function (value, element) {
    return this.optional(element) || /^([0-9A-F]{2}[:-]?){5}([0-9A-F]{2})$/i.test(value);
}, "Please provide a valid MAC address.");

let numberOnlyNormalizer = function (value) {
    return $.trim(value.replace(/\D+/g, ''))
}

let alphaNumericOnlyNormalizer = function (value) {
    return $.trim(value.replace(/[^a-z0-9]+/gi, ''))
}

let getRootElement = function (el, selector) {
    el = $(el)
    if (!el.is(selector))
        el = el.parents(selector)
    return el
}

let validateErrorPlacement = function (error, element) {
    error.appendTo(element.parents('.form-group'))
}
