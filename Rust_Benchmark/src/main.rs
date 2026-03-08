use std::fs::File;
use std::io::Write;
use std::time::Instant;

fn bubble_sort(arr: &mut [i32]) {
    let n = arr.len();
    for i in 0..n {
        let mut swapped = false;
        for j in 0..n - i - 1 {
            if arr[j] > arr[j + 1] {
                arr.swap(j, j + 1);
                swapped = true;
            }
        }
        if !swapped {
            break;
        }
    }
}

fn selection_sort(arr: &mut [i32]) {
    let n = arr.len();
    for i in 0..n {
        let mut min_idx = i;
        for j in i + 1..n {
            if arr[min_idx] > arr[j] {
                min_idx = j;
            }
        }
        arr.swap(i, min_idx);
    }
}

fn insertion_sort(arr: &mut [i32]) {
    let n = arr.len();
    for i in 1..n {
        let key = arr[i];
        let mut j = i as isize - 1;
        while j >= 0 && arr[j as usize] > key {
            arr[(j + 1) as usize] = arr[j as usize];
            j -= 1;
        }
        arr[(j + 1) as usize] = key;
    }
}

fn merge_sort(arr: &mut [i32]) {
    let n = arr.len();
    if n == 0 { return; }
    let mut temp = vec![0; n];
    merge_sort_recursive(arr, &mut temp, 0, n - 1);
}

fn merge_sort_recursive(arr: &mut [i32], temp: &mut [i32], left: usize, right: usize) {
    if left < right {
        let mid = left + (right - left) / 2;
        merge_sort_recursive(arr, temp, left, mid);
        merge_sort_recursive(arr, temp, mid + 1, right);
        merge(arr, temp, left, mid, right);
    }
}

fn merge(arr: &mut [i32], temp: &mut [i32], left: usize, mid: usize, right: usize) {
    for x in left..=right {
        temp[x] = arr[x];
    }
    let mut i = left;
    let mut j = mid + 1;
    let mut k = left;

    while i <= mid && j <= right {
        if temp[i] <= temp[j] {
            arr[k] = temp[i];
            i += 1;
        } else {
            arr[k] = temp[j];
            j += 1;
        }
        k += 1;
    }
    while i <= mid {
        arr[k] = temp[i];
        k += 1;
        i += 1;
    }
}

fn quick_sort(arr: &mut [i32]) {
    let n = arr.len();
    if n > 0 {
        quick_sort_recursive(arr, 0, (n - 1) as isize);
    }
}

fn quick_sort_recursive(arr: &mut [i32], low: isize, high: isize) {
    if low < high {
        let pi = partition(arr, low, high);
        quick_sort_recursive(arr, low, pi - 1);
        quick_sort_recursive(arr, pi + 1, high);
    }
}

fn partition(arr: &mut [i32], low: isize, high: isize) -> isize {
    let mid = low + (high - low) / 2;
    arr.swap(mid as usize, high as usize);
    let pivot = arr[high as usize];
    let mut i = low - 1;
    for j in low..high {
        if arr[j as usize] < pivot {
            i += 1;
            arr.swap(i as usize, j as usize);
        }
    }
    arr.swap((i + 1) as usize, high as usize);
    i + 1
}

// Simulador pseudo-randômico (LCG) nativo para evitar crates demoradas
struct LcgRng {
    state: u64,
}
impl LcgRng {
    fn new(seed: u64) -> Self {
        Self { state: seed }
    }
    fn next_u32(&mut self) -> u32 {
        self.state = self.state.wrapping_mul(6364136223846793005).wrapping_add(1);
        (self.state >> 32) as u32
    }
    fn next_in_range(&mut self, min: i32, max: i32) -> i32 {
        let range = (max - min) as u32;
        let val = self.next_u32() % range;
        min + val as i32
    }
}

fn generate_random_array(size: usize, rng: &mut LcgRng) -> Vec<i32> {
    let mut arr = Vec::with_capacity(size);
    for _ in 0..size {
        arr.push(rng.next_in_range(0, (size * 2) as i32));
    }
    arr
}

fn generate_sorted_array(size: usize) -> Vec<i32> {
    (0..size).map(|i| i as i32).collect()
}

fn generate_reverse_sorted_array(size: usize) -> Vec<i32> {
    (0..size).map(|i| (size - i) as i32).collect()
}

fn main() {
    let tamanhos = [1000, 10000, 100000];
    let k_amostras = 5;
    let tipos = ["Aleatório", "Crescente", "Decrescente"];
    let algoritmos = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"];
    
    let funcs: Vec<fn(&mut [i32])> = vec![
        bubble_sort,
        selection_sort,
        insertion_sort,
        merge_sort,
        quick_sort,
    ];
    
    let mut rng = LcgRng::new(42);
    
    println!("Iniciando bateria de testes em Rust ({} amostras).", k_amostras);

    let mut json_output = String::from("{\n");

    for a in 0..algoritmos.len() {
        json_output.push_str(&format!("  \"{}\": {{\n", algoritmos[a]));
        for t in 0..tipos.len() {
            json_output.push_str(&format!("    \"{}\": {{\n", tipos[t]));
            for s in 0..tamanhos.len() {
                let tamanho = tamanhos[s];
                println!("\nTipo: {} | Tamanho: {} | Gerando {} vetores amostrais...", tipos[t], tamanho, k_amostras);
                
                let mut vetores_originais = Vec::new();
                for _ in 0..k_amostras {
                    if t == 0 {
                        vetores_originais.push(generate_random_array(tamanho, &mut rng));
                    } else if t == 1 {
                        vetores_originais.push(generate_sorted_array(tamanho));
                    } else {
                        vetores_originais.push(generate_reverse_sorted_array(tamanho));
                    }
                }

                let mut tempos_execucoes = Vec::new();
                print!("Executando {} ({}x)... ", algoritmos[a], k_amostras);

                for k in 0..k_amostras {
                    let mut vetor_teste = vetores_originais[k].clone();
                    
                    let start = Instant::now();
                    funcs[a](&mut vetor_teste);
                    let elapsed = start.elapsed();
                    
                    tempos_execucoes.push(elapsed.as_secs_f64());
                }

                let sum: f64 = tempos_execucoes.iter().sum();
                let media = sum / k_amostras as f64;
                
                let mut sum_of_squares = 0.0;
                for tempo in &tempos_execucoes {
                    sum_of_squares += (*tempo - media) * (*tempo - media);
                }
                let desvio = if k_amostras > 1 {
                    (sum_of_squares / (k_amostras - 1) as f64).sqrt()
                } else {
                    0.0
                };

                println!("[Média: {:.4}s | StdDev: ±{:.4}s]", media, desvio);

                json_output.push_str(&format!("      \"{}\": {{\n        \"media\": {:.8},\n        \"desvio_padrao\": {:.8}\n      }}", 
                    tamanho, media, desvio));
                    
                if s < tamanhos.len() - 1 {
                    json_output.push_str(",");
                }
                json_output.push_str("\n");
            }
            json_output.push_str("    }");
            if t < tipos.len() - 1 {
                json_output.push_str(",");
            }
            json_output.push_str("\n");
        }
        json_output.push_str("  }");
        if a < algoritmos.len() - 1 {
            json_output.push_str(",");
        }
        json_output.push_str("\n");
    }
    json_output.push_str("}\n");

    let mut file = File::create("resultados_rust.json").expect("Unable to create file");
    file.write_all(json_output.as_bytes()).expect("Unable to write data");
    println!("\nTestes Rust concluídos. Resultados salvos em 'resultados_rust.json'.");
}
