## Requirements
- pyserial
- mss
- pillow

Install with
```bash
pip install pyserial mss pillow
```

## Usage (_Windows_)
1. Setup the ARDUINO as described in the [schematics](https://github.com/unfuug/screen2led/blob/main/schematics.pdf) and connect it via USB
2. Compile and push the ARDUINO code (`arduino/arduino.ino`) 
3. Change the PORT and BAUDRATE in the `main()` in `script2.py` to match your ARDUINO
4. Run `script2.py`

## Acknowledgements
This repo contains modified code from [Pylette](https://github.com/qTipTip/Pylette) and [color-thief-py](https://github.com/fengsp/color-thief-py).