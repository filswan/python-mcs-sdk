from upload.free_upload import FreeUpload

w = "0x61c3e03dbed55f5DE213732e816F8A8Fd6E9bfF0"
p = "9b7b90e22f0ac48611e4c9e9a09b008c013780a8bb28e213b60e5ad15953258c"
a = "https://rpc-mumbai.maticvigil.com"
f = "C:/Users/chenz/Pictures/Saved Pictures/Chun-Li-Street-Fighter-IV-advertisment-art2.jpg" 

up = FreeUpload(w,p,a,f)
up.free_upload()