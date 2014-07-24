""" ESC/POS Commands (Constants) """

# Feed control sequences
CTL_LF     = b'\x0a'              # Print and line feed
CTL_FF     = b'\x0c'              # Form feed
CTL_CR     = b'\x0d'              # Carriage return
CTL_HT     = b'\x09'              # Horizontal tab
CTL_SET_HT = b'\x1b\x44'          # Set horizontal tab positions
CTL_VT     = b'\x1b\x64\x04'      # Vertical tab
# Printer hardware
HW_INIT    = b'\x1b\x40'          # Clear data in buffer and reset modes
HW_SELECT  = b'\x1b\x3d\x01'      # Printer select
HW_RESET   = b'\x1b\x3f\x0a\x00'  # Reset printer hardware
# Cash Drawer
CD_KICK_2  = b'\x1b\x70\x00'      # Sends a pulse to pin 2 [] 
CD_KICK_5  = b'\x1b\x70\x01'      # Sends a pulse to pin 5 [] 
# Paper
PAPER_FULL_CUT  = b'\x1d\x56\x00' # Full cut paper
PAPER_PART_CUT  = b'\x1d\x56\x01' # Partial cut paper
# Text format   
TXT_NORMAL      = b'\x1b\x21\x00' # Normal text
TXT_2HEIGHT     = b'\x1b\x21\x10' # Double height text
TXT_2WIDTH      = b'\x1b\x21\x20' # Double width text
TXT_4SQUARE     = b'\x1b\x21\x30' # Quad area text
TXT_UNDERL_OFF  = b'\x1b\x2d\x00' # Underline font OFF
TXT_UNDERL_ON   = b'\x1b\x2d\x01' # Underline font 1-dot ON
TXT_UNDERL2_ON  = b'\x1b\x2d\x02' # Underline font 2-dot ON
TXT_BOLD_OFF    = b'\x1b\x45\x00' # Bold font OFF
TXT_BOLD_ON     = b'\x1b\x45\x01' # Bold font ON
TXT_FONT_A      = b'\x1b\x4d\x00' # Font type A
TXT_FONT_B      = b'\x1b\x4d\x01' # Font type B
TXT_ALIGN_LT    = b'\x1b\x61\x00' # Left justification
TXT_ALIGN_CT    = b'\x1b\x61\x01' # Centering
TXT_ALIGN_RT    = b'\x1b\x61\x02' # Right justification
# Char code table
CHARCODE_PC437  = b'\x1b\x74\x00' # USA: Standard Europe
CHARCODE_JIS    = b'\x1b\x74\x01' # Japanese Katakana
CHARCODE_PC850  = b'\x1b\x74\x02' # Multilingual
CHARCODE_PC860  = b'\x1b\x74\x03' # Portuguese
CHARCODE_PC863  = b'\x1b\x74\x04' # Canadian-French
CHARCODE_PC865  = b'\x1b\x74\x05' # Nordic
CHARCODE_WEU    = b'\x1b\x74\x06' # Simplified Kanji, Hirakana
CHARCODE_GREEK  = b'\x1b\x74\x07' # Simplified Kanji
CHARCODE_HEBREW = b'\x1b\x74\x08' # Simplified Kanji
CHARCODE_PC1252 = b'\x1b\x74\x11' # Western European Windows Code Set
CHARCODE_PC866  = b'\x1b\x74\x12' # Cirillic #2
CHARCODE_PC852  = b'\x1b\x74\x13' # Latin 2
CHARCODE_PC858  = b'\x1b\x74\x14' # Euro
CHARCODE_THAI42 = b'\x1b\x74\x15' # Thai character code 42
CHARCODE_THAI11 = b'\x1b\x74\x16' # Thai character code 11
CHARCODE_THAI13 = b'\x1b\x74\x17' # Thai character code 13
CHARCODE_THAI14 = b'\x1b\x74\x18' # Thai character code 14
CHARCODE_THAI16 = b'\x1b\x74\x19' # Thai character code 16
CHARCODE_THAI17 = b'\x1b\x74\x1a' # Thai character code 17
CHARCODE_THAI18 = b'\x1b\x74\x1b' # Thai character code 18
# Barcode format
BARCODE_TXT_OFF = b'\x1d\x48\x00' # HRI barcode chars OFF
BARCODE_TXT_ABV = b'\x1d\x48\x01' # HRI barcode chars above
BARCODE_TXT_BLW = b'\x1d\x48\x02' # HRI barcode chars below
BARCODE_TXT_BTH = b'\x1d\x48\x03' # HRI barcode chars both above and below
BARCODE_FONT_A  = b'\x1d\x66\x00' # Font type A for HRI barcode chars
BARCODE_FONT_B  = b'\x1d\x66\x01' # Font type B for HRI barcode chars
BARCODE_HEIGHT  = b'\x1d\x68\x64' # Barcode Height [1-255]
BARCODE_WIDTH   = b'\x1d\x77\x03' # Barcode Width  [2-6]
BARCODE_UPC_A   = b'\x1d\x6b\x00' # Barcode type UPC-A
BARCODE_UPC_E   = b'\x1d\x6b\x01' # Barcode type UPC-E
BARCODE_EAN13   = b'\x1d\x6b\x02' # Barcode type EAN13
BARCODE_EAN8    = b'\x1d\x6b\x03' # Barcode type EAN8
BARCODE_CODE39  = b'\x1d\x6b\x04' # Barcode type CODE39
BARCODE_ITF     = b'\x1d\x6b\x05' # Barcode type ITF
BARCODE_NW7     = b'\x1d\x6b\x06' # Barcode type NW7
# Image format  
S_RASTER_N      = b'\x1d\x76\x30\x00' # Set raster image normal size
S_RASTER_2W     = b'\x1d\x76\x30\x01' # Set raster image double width
S_RASTER_2H     = b'\x1d\x76\x30\x02' # Set raster image double height
S_RASTER_Q      = b'\x1d\x76\x30\x03' # Set raster image quadruple
# Printing Density
PD_N50          = b'\x1d\x7c\x00' # Printing Density -50%
PD_N37          = b'\x1d\x7c\x01' # Printing Density -37.5%
PD_N25          = b'\x1d\x7c\x02' # Printing Density -25%
PD_N12          = b'\x1d\x7c\x03' # Printing Density -12.5%
PD_0            = b'\x1d\x7c\x04' # Printing Density  0%
PD_P50          = b'\x1d\x7c\x08' # Printing Density +50%
PD_P37          = b'\x1d\x7c\x07' # Printing Density +37.5%
PD_P25          = b'\x1d\x7c\x06' # Printing Density +25%
PD_P12          = b'\x1d\x7c\x05' # Printing Density +12.5%
