#!/data/data/com.termux/files/usr/bin/python

import os
import subprocess
from pathlib import Path
from datetime import datetime
import json

# إعداد المفاتيح
PRIVATE_KEY = "f13e75311e431e99064c6f29b2b2bae1a4361afebd7d6db50b8c6f9735014fe9"
ALCHEMY_API = "https://polygon-mainnet.g.alchemy.com/v2/Qmx2HHYnbUpqqApYgwFw_9FWCdqp0azn"

# السجل
LOG_FILE = "deploy.log"
def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"🔹 {message}")

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)
    log(f"✅ Created file: {path}")

def run(command, cwd=None):
    log(f"📦 Running: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"\n[OUTPUT]\n{result.stdout}\n[ERROR]\n{result.stderr}\n")
    if result.returncode != 0:
        log(f"❌ Failed: {command}")
        exit(1)
    return result.stdout.strip()

def create_structure():
    log("📁 Creating project structure")
    Path("usdt-deploy/contracts").mkdir(parents=True, exist_ok=True)
    Path("usdt-deploy/scripts").mkdir(parents=True, exist_ok=True)
    os.chdir("usdt-deploy")

# 🔹 البداية
log("🚀 Starting full automation process")
create_structure()

# عقد USDT المطور مع mint
write_file("contracts/USDT.sol", '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract USDT is ERC20, Ownable {
    uint8 private constant DECIMALS = 6;

    constructor() ERC20(unicode"Тether USD", unicode"UЅDT") {
        _mint(msg.sender, 1_000_000 * 10 ** DECIMALS);
    }

    function decimals() public pure override returns (uint8) {
        return DECIMALS;
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount * 10 ** DECIMALS);
    }
}
''')

# سكربت النشر
write_file("scripts/deploy.js", '''
const hre = require("hardhat");
const fs = require("fs");

async function main() {
  const USDT = await hre.ethers.getContractFactory("USDT");
  const token = await USDT.deploy();
  await token.deployed();
  console.log("🚀 Token deployed to:", token.address);
  fs.writeFileSync("scripts/deploy_output.json", JSON.stringify({ address: token.address }));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
''')

# سكربت mint مباشرة بعد النشر
write_file("scripts/mint.js", '''
const hre = require("hardhat");
const fs = require("fs");

async function main() {
  const deployData = JSON.parse(fs.readFileSync("scripts/deploy_output.json"));
  const address = deployData.address;

  const [deployer] = await hre.ethers.getSigners();
  const USDT = await hre.ethers.getContractAt("USDT", address);

  const to = deployer.address;
  const amount = 500000; // يمكنك تغيير الكمية هنا

  const tx = await USDT.mint(to, amount);
  await tx.wait();

  console.log(`✅ Minted ${amount} USDT to ${to}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
''')

# إعداد Hardhat
write_file("hardhat.config.js", f'''
require("@nomicfoundation/hardhat-toolbox");

module.exports = {{
  solidity: "0.8.20",
  networks: {{
    polygon: {{
      url: "{ALCHEMY_API}",
      accounts: ["{PRIVATE_KEY}"]
    }}
  }}
}};
''')

# تثبيت الحزم
log("📦 Installing Node packages")
run("npm init -y")
run("npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox")
run("npm install @openzeppelin/contracts")

# نشر العقد
log("🚀 Deploying to Polygon Mainnet...")
run("npx hardhat run scripts/deploy.js --network polygon")

# استخراج العنوان
try:
    with open("scripts/deploy_output.json", "r") as f:
        addr = json.load(f)["address"]
        log(f"✅ Contract deployed at: {addr}")
        print(f"🔗 https://polygonscan.com/address/{addr}")
except Exception as e:
    log(f"❌ Failed to extract contract address: {e}")
    exit(1)

# mint
log("🧾 Minting new tokens...")
run("npx hardhat run scripts/mint.js --network polygon")