var setup = function() {
  println("Hello from setup");
  draw();
};

var draw = function() {
  background(32, 32, 128);
  fill(0, 0, 0);
  ellipse(200, 200, 200, 200);
  fill(32, 0, 32);
  triangle(200, 0, 0, 400, 400, 400);
  rect(0, 0, 200, 200);
  text("Hello", 200, 200);
};
