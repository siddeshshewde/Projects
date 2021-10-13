use ansi_term::Color::Green;
use sysinfo::{ComponentExt, ProcessorExt, System, SystemExt};
use termion::{cursor::DetectCursorPos, raw::IntoRawMode};

fn main() {
    println!(" ");

    let left_pad = 25;
    let mut stdout = std::io::stdout().into_raw_mode().unwrap();
    let mut sys = System::new_all();

    sys.refresh_all();

    println!("{}",Green.paint("     /\\\r\n    ( /   X X    ()\r\n     \\  __[]__  /\r\n      -/   \"   \\-\r\n     /-|       |-\\\r\n    / /-\\     /-\\ \\\r\n     / /-`---\'-\\ \\\r\n      /         \\\r\n") );

    let mut cursor_row = stdout.cursor_pos().unwrap().1;

    cursor_row = cursor_row - 9;
    println!(
        "{}{} : {}\r",
        termion::cursor::Goto(left_pad, cursor_row),
        Green.bold().paint("OS"),
        sys.name().unwrap()
    );
    cursor_row = cursor_row + 1;
    println!(
        "{}{} : {}\r",
        termion::cursor::Goto(left_pad, cursor_row),
        Green.bold().paint("kernel"),
        sys.kernel_version().unwrap()
    );
    cursor_row = cursor_row + 1;
    println!(
        "{}{} : {}\r",
        termion::cursor::Goto(left_pad, cursor_row),
        Green.bold().paint("Host"),
        sys.host_name().unwrap()
    );
    cursor_row = cursor_row + 1;
    println!(
        "{}{} : {}\r",
        termion::cursor::Goto(left_pad, cursor_row),
        Green.bold().paint("CPU"),
        sys.processors()[0].brand()
    );
    cursor_row = cursor_row + 1;
    println!(
        "{}{} : {}\r",
        termion::cursor::Goto(left_pad, cursor_row),
        Green.bold().paint("Cores"),
        sys.processors().len()
    );
    cursor_row = cursor_row + 1;

    let mut usage = 0;

    for processor in sys.processors() {
        usage = usage + processor.cpu_usage() as usize;
    }
    println!(
        "{}{} : {}%\r",
        termion::cursor::Goto(left_pad, cursor_row),
        Green.bold().paint("Usage"),
        usage / sys.processors().len()
    );
    cursor_row = cursor_row + 1;

    for component in sys.components() {
        if component.label().contains("package id") {
            println!(
                "{}{} : {}c\r",
                termion::cursor::Goto(left_pad, cursor_row),
                Green.bold().paint("temp"),
                component.temperature()
            );
            cursor_row = cursor_row + 1;
            break;
        }
    }
    println!(
        "{}{} : {}MB/{}MB\r",
        termion::cursor::Goto(left_pad, cursor_row),
        Green.bold().paint("Ram"),
        sys.used_memory() / 1024,
        sys.total_memory() / 1024
    );
}
