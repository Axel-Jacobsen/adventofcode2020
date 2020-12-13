use std::fs;
use std::env;


#[derive(Debug)]
struct OpVal {
    op: String,
    val: i32,
    executed: bool
}


impl OpVal {
    fn new(opval_str: &str) -> OpVal {
        let opval_str: Vec<&str> = opval_str.split(" ").collect();
        let op = opval_str[0].to_string();
        let executed: bool = true;  // there is certainly a cleaner way to do this
        match opval_str[1].replace("+", "").parse::<i32>() {
            Ok(val) => return OpVal{op, val, executed},
            Err(_) => panic!("parsing error")
        }
    }
}


fn evaluate(tape: Vec<OpVal>) -> Result<i32, String> {
    let mut idx: usize = 0;
    let mut global_accumulator: i32 = 0;

    loop {
        if tape[idx].executed {
            let s = format!("INFINITE LOOP DETECTED: idx = {}, accumulator = {}", idx, global_accumulator);
            Err(s);
        }
        else if idx >= tape.len() {
            return Ok(global_accumulator);
        }

        let mut opval: OpVal = tape[idx];
        opval.executed = true;
        if opval.op == "nop" {
            idx = idx + 1;
        } else if opval.op == "acc" {
            global_accumulator += opval.val;
            break;
        }
    }

    return Ok(global_accumulator);
}


fn main() {
    let args: Vec<String> = env::args().collect();
    let filename: &String = &args[1];

    let contents = fs::read_to_string(filename)
        .expect("error reading file");

    let tape: Vec<&OpVal> = contents.split("\n")
                                   .filter(|x| *x != "")
                                   .map(|x| OpVal::new(x))
                                   .collect();
    println!("{:?}", tape);
}
