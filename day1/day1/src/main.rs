use std::fs;

fn f() -> u32 {
    let contents: Vec<u32> = fs::read_to_string("../../input.txt")
        .expect("Something went wrong reading the file")
        .split(' ')
        .filter(|s| !s.is_empty())
        .map(|s| s.parse().unwrap())
        .collect();

    for i in 0..contents.len() {
        for j in 0..contents.len() {
            for k in 0..contents.len() {
                if contents[i] + contents[j] + contents[k] == 2020 {
                    return contents[i] * contents[j] * contents[k];
                }
            }
        }
    }
    return 0;
}

fn main() {
    println!("{}", f());
}
