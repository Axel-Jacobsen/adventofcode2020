use std::fs;
use std::env;


#[derive(Debug)]
struct OpVal {
    op: String,
    val: i16
}


impl OpVal {
    fn new(opval_str: &str) -> OpVal {
        println!("{}", opval_str);
        let opval_str: Vec<&str> = opval_str.split(" ").collect();
        let op = opval_str[0].to_string();
        match opval_str[1].replace("+", "").parse::<i16>() {
            Ok(val) => return OpVal{op, val},
            Err(_) => panic!("parsing error")
        }
    }
}


fn main() {
    let args: Vec<String> = env::args().collect();
    let filename: &String = &args[1];

    let contents = fs::read_to_string(filename)
        .expect("error reading file");

    let tape: Vec<OpVal> = contents.split("\n")
                                   .filter(|x| *x != "")
                                   .map(|x| OpVal::new(x))
                                   .collect();
    println!("{:?}", tape);
}
