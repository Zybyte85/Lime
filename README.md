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
const str GREETING = "Hello, world!"

void main() {
    let x = 5 # Inferred type
    let y = 10

    print("{GREETING}")
    print("The sum of {x} and {y} is {add(x, y)}")

    if multiply(3, 3) > add(3, 3) {
        print("3*3 is greater than 3+3")

    var int i = 0
    while i < 10 {
        print("{i}")
        i = i + 1
    }
}

int add(int a, int b) {
    return a + b
}

int multiply(int a, int b) {
    return a * b
}
```
Would transpile into:
```
const GREETING: &str = "Hello, world!";
fn main() -> () {
    let x = 5;
    let y = 10;
    println!("{GREETING}");
    println!("The sum of {x} and {y} is {}", add(x, y));
    if multiply(3, 3) > add(3, 3) {
        println!("3*3 is greater than 3+3");
    }
    let mut i: i32 = 0;
    while i <= 10 {
        println!("{i}");
        i = i + 1
    }
}
fn add(a: i32, b: i32) -> i32 {
    return a + b;
}
fn multiply(a: i32, b: i32) -> i32 {
    return a * b;
}
```
Which would then compile into a binary and output
```
Hello, world!
The sum of 5 and 10 is 15
3*3 is greater than 3+3
0
1
2
3
4
5
6
7
8
9
10
```
This is about as much as the language can do for now, because, like I said, it is in a VERY early stage.

## Why
I have always liked Python. I love how fast you can make somthing and read other people's code, but it's really slow as a language. My hope is that once this gets to a usable state, it could be a good replacement that lets people build high-performance applications faster.

## Contributing
If you are interested in it, and know how to, please contribute. It helps a lot and I would very much appriciate it :)

## Roadmap
- [ ] Finish basic language features
  - [x] Functions
  - [x] Conditional statements
  - [ ] Switch statements
  - [ ] Loops
  - [ ] Dot notation
- [ ] Add support for using Rust libraries
