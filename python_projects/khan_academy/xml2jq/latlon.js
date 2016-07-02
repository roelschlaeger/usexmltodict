// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

var latlon = function(input_value, pm) {
    var negative = (input_value < 0);
    var n = Math.abs(input_value);
    var degrees = Math.floor(n);
    var minutes = (n - degrees) * 60.;
    var c;
    if (negative) {
        c = pm.split("")[1];
    } else {
        c = pm.split("")[0];
    }
    return c + degrees.toFixed(0) + "° " + minutes.toFixed(3);
};

var latstr = function(n) {
    return latlon(n, "NS")
};

var lonstr = function(n) {
    return latlon(n, "EW")
};
