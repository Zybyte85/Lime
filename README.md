<div align=center>
  <img src=assets/icons/lime.svg alt="Lime logo" height=200>
  <h1>Lime</h1>
  <a href=https://github.com/Zybyte85/Lime/#what>What?</a>
  ·
  <a href=https://github.com/Zybyte85/Lime/#why>Why?</a>
</div>

## What
Lime is a language with Python-like syntax that transpiles to Rust. It is currently in a very early stage, and needs much work before it is ready.

### Example
```
void main() {
    str greeting = "Hello, world!"
    int x = 5
    int y = 10

    print("{greeting}")
    print("The sum of {x} and {y} is {add(x, y)}")
}

int add(int a, int b) {
    return a + b
}
```
Would transpile into:
```
fn main() -> () {
    let greeting: &str = "Hello, world!";
    let x: i32 = 5;
    let y: i32 = 10;
    println!("{greeting}");
    println!("The sum of {x} and {y} is {}", add(x, y));
}
fn add(a: i32, b: i32) -> i32 {
    return a + b;
}
```
Which would then compile into a binary and output
```
Hello, world!
The sum of 5 and 10 is 15
```
This is about as much as the language can do for now, because, like I said, it is in a VERY early stage.

## Why
I have always liked Python. I love how fast you can make somthing and read other people's code, but it's really slow as a language. My hope is that once this gets to a usable state, it could be a good replacement that lets people build high-performance applications faster.

## Contributing
If you are interested in it, and know how to, please contribute. It helps a lot and I would very much appriciate it :)
