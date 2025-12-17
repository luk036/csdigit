use clap::{Parser, Subcommand};
use csdigit::{to_csd, to_csdnnz, to_decimal};
use env_logger;
use log;

#[derive(Parser)]
#[command(name = "csdigit")]
#[command(about = "Converts a decimal to a CSD format", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
    
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,
}

#[derive(Subcommand)]
enum Commands {
    /// Convert decimal to CSD format
    ToCsd {
        /// Decimal number to convert
        decimal: f64,
        
        /// Number of decimal places
        #[arg(short, long, default_value = "4")]
        places: i32,
    },
    /// Convert decimal to CSD format with non-zero limit
    ToCsdnnz {
        /// Decimal number to convert
        decimal: f64,
        
        /// Maximum number of non-zero digits
        #[arg(short, long, default_value = "4")]
        nnz: i32,
    },
    /// Convert CSD string to decimal
    ToDecimal {
        /// CSD string to convert
        csdstr: String,
    },
}

fn setup_logging(verbose: u8) {
    let log_level = match verbose {
        0 => log::LevelFilter::Warn,
        1 => log::LevelFilter::Info,
        2 => log::LevelFilter::Debug,
        _ => log::LevelFilter::Trace,
    };
    
    env_logger::Builder::new()
        .filter_level(log_level)
        .format_timestamp(None)
        .format_module_path(false)
        .init();
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    
    setup_logging(cli.verbose);
    log::debug!("Starting CSD calculations...");
    
    match cli.command {
        Commands::ToCsd { decimal, places } => {
            let ans = to_csd(decimal, places);
            println!("{}", ans);
        }
        Commands::ToCsdnnz { decimal, nnz } => {
            let ans = to_csdnnz(decimal, nnz);
            println!("{}", ans);
        }
        Commands::ToDecimal { csdstr } => {
            let ans = to_decimal(&csdstr);
            println!("{}", ans);
        }
    }
    
    log::info!("Script ends here");
    Ok(())
}