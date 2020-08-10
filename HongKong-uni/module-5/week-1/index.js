var rect = require('./rectangle');

function solveRect(l,b){
	console.log("Solving for rectangle with l= " + l + " and b = " + b);

	rect(l, b, (err, rectangle) => 
	{
		if (err)
		{
			console.log("ERROR: ", err.message);
		} else
		{
			console.log("Area of rectangle of dimensions l = "
			+ l + "and b = " + b + " is " + rectangle.area);

			console.log("Perimeter of rectangle of dimensions l = "
			+ l + "and b = " + b + " is " + rectangle.perimeter);
		}
	}
	)

	console.log("This statement illustrates async programming. The rect function has been called.");
}

solveRect(2,4);
solveRect(3,5);
solveRect(0,5);
solveRect(-3,2);