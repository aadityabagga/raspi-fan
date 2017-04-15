With the particular [relay switch](https://www.eprolabs.com/product/single-relay-module/) that I have, as soon as the GPIO pin is set to output mode (irrespective of the fact whether the output is low or high), the fan switches on.

So the `fanON()` and `fanOFF()` functions have been modified to set the GPIO pin state to output and input mode respectively, rather than setting pin output to high and low. This also means that one cannot check if the fan is on or off based on the value of the GPIO output.
