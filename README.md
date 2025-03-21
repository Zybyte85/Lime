<div align=center>
  <img src=Lime.png alt="Lime logo" height=200>
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
        print("Hello World!")
}
```
Would transpile into:
```
fn main() -> () {
    println!("Hello World!");
}
```
Which would then compile into a binary and output
`Hello World!`
This is about as much as the language can do for now, because, like I said, it is in a VERY early stage.

## Why
I have always liked Python. I love how fast you can make somthing and read other people's code, but it's really slow as a language. My hope is that once this gets to a usable state, it could be a good replacement that lets people build high-performance applications faster.

## Contributing
If you are interested in it, and know how to, please contribute. It helps a lot and I would very much appriciate it :)
