// console.log(process.argv)
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

var item;
var sum;

sum = 0;
for (var i=2; i<process.argv.length; i++) {
// item = process.argv[i].valueOf();
   sum += Number(process.argv[i]);
};

console.log(sum);
