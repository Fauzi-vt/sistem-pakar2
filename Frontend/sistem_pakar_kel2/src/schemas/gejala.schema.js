import * as yup from 'yup'

export const gejalaSchema = yup.object({
  kode: yup.string()
    .required('Kode gejala wajib diisi')
    .matches(/^G\d+$/, 'Format kode harus diawali huruf G diikuti angka (contoh: G01)'),
  nama: yup.string()
    .required('Nama gejala wajib diisi')
    .min(3, 'Nama gejala minimal harus 3 karakter')
})
