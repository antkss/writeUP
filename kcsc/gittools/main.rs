use std::io::{self, Write};
use std::fs;
use rand::Rng;

trait MyTraitI8 {
    fn add(&mut self, other: i8);
    fn sub(&mut self, other: i8);
    fn is_zero(self) -> bool;
}

impl MyTraitI8 for i8 {
    fn add(&mut self, other: i8) {
        *self += other;
    }
    fn sub(&mut self, other: i8) {
        *self -= other;
    }
    fn is_zero(self) -> bool{
        if self==0 {
            true
        } else {
            false
        }
    }
}

trait MyTraitArrI8 {
    fn swap_number(&mut self, idx1: usize, idx2: usize);
    fn shuffle(&mut self, arr_len: usize);
    fn is_equal(&mut self, arr_final: &[i8], arr_len: usize) -> bool;
}

impl MyTraitArrI8 for [i8] {
    fn swap_number(&mut self, idx1: usize, idx2: usize) {
        let arr_ptr = self.as_mut_ptr();
        let tmp: i8;
        unsafe {
            tmp = *arr_ptr.add(idx1);
            *arr_ptr.add(idx1) = *arr_ptr.add(idx2);
            *arr_ptr.add(idx2) = tmp;
        }
    }
    fn shuffle(&mut self, arr_len: usize) {
        let mut rng = rand::thread_rng();
        let mut tmp_vec = self[0..arr_len as usize].to_vec();
        let mut randnum: usize;

        for i in 0..arr_len {
            randnum = rng.gen_range(0..tmp_vec.len());
            self[i] = tmp_vec[randnum];
            tmp_vec.remove(randnum);
        }
    }
    fn is_equal(&mut self, arr_final: &[i8], arr_len: usize) -> bool {
        let mut equal = true;

        for i in 0..arr_len {
            if self[i]!=arr_final[i] {
                equal = false;
                break
            }
        }
        equal
    }
}

fn read_long() -> i64 {
    let mut buf = String::new();
    let val: i64;

    loop {
        buf.clear();
        io::stdin().read_line(&mut buf).expect("Failed to read_line");
        match buf.trim().parse::<i64>() {
            Ok(n) => {
                val = n;
                break;
            },
            Err(_) => {
                println!("Invalid digit!");
            }
        }    
    }
    val
}

fn read_char() -> i8 {
    let mut buf = String::new();
    let val: i8;

    loop {
        buf.clear();
        io::stdin().read_line(&mut buf).expect("Failed to read_line");
        match buf.trim().parse::<i8>() {
            Ok(n) => {
                val = n;
                break;
            },
            Err(_) => {
                println!("Invalid digit!");
            }
        }    
    }
    val
}

fn menu()
{
    println!("1. Add number");
    println!("2. Subtract number");
    println!("3. Is number zero");
    println!("4. Swap number");
    println!("5. Submit");
    print!("> ");
    io::stdout().flush().unwrap();
}

fn main() {
    let mut arr: [i8; 100] = [0; 100];
    let mut arr_final: [i8; 100] = [0; 100];
    let mut arr_len: i64;
    let mut val: i8;
    let mut idx: i64;
    let mut idx2: i64;

    println!("Guessing game!");
    println!("---------------\nIn this game, you will first enter maximum 100 numbers and I will\nrandomly rearrange all 100 number. Your job is to guess it with\n4 functions available!\n---------------\n");
    loop {
        print!("Number of element: ");
        io::stdout().flush().unwrap();
        arr_len = read_long();
        if (arr_len) <= 0 {
            println!("Please input again!");
        } else {
            break;
        }
    }

    for i in 0..(arr_len as usize) {
        print!("arr[{}]=", i);
        io::stdout().flush().unwrap();
        arr[i] = read_char();
    }
    
    arr.shuffle(arr_len as usize);

    loop {
        menu();
        match read_long() {
            1 => {
                print!("Index: ");
                io::stdout().flush().unwrap();
                idx = read_long();
                print!("Value: ");
                io::stdout().flush().unwrap();
                val = read_char();

                arr[idx as usize].add(val);
            },
            2 => {
                print!("Index: ");
                io::stdout().flush().unwrap();
                idx = read_long();
                print!("Value: ");
                io::stdout().flush().unwrap();
                val = read_char();

                arr[idx as usize].sub(val);
            },
            3 => {
                print!("Index: ");
                io::stdout().flush().unwrap();
                idx = read_long();

                if arr[idx as usize].is_zero() {
                    println!("arr[{}] is zero", idx);
                } else {
                    println!("arr[{}] is NOT zero", idx);
                }
            },
            4 => {
                print!("Index 1: ");
                io::stdout().flush().unwrap();
                idx = read_long();

                print!("Index 2: ");
                io::stdout().flush().unwrap();
                idx2 = read_long();

                arr.swap_number(idx as usize, idx2 as usize);
            },
            5 => break,
            _ => println!("Invalid choice"),
        }
    }

    println!("You only have 1 chance to win this game!");
    for i in 0..(arr_len as usize) {
        print!("arr[{}]=", i);
        io::stdout().flush().unwrap();
        arr_final[i] = read_char();
    }
    if arr.is_equal(&arr_final, arr_len as usize) {
        print!("You win!!!\nHere is your prize: ");
        io::stdout().flush().unwrap();
        let data = fs::read_to_string("flag.txt").expect("flag.txt: File not found");
        println!("{}", data);
    } else {
        println!("Nah, you 🐥");
    }

}
