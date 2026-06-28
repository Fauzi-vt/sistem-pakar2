import * as yup from 'yup'

export const penyakitSchema = yup.object({
  kode: yup.string()
    .required('Kode penyakit wajib diisi')
    .matches(/^P\d+$/, 'Format kode harus diawali huruf P diikuti angka (contoh: P01)'),
  nama: yup.string()
    .required('Nama penyakit wajib diisi')
    .min(3, 'Nama penyakit minimal harus 3 karakter'),
  deskripsi: yup.string().nullable().default(''),
  solusi: yup.string()
    .required('Saran medis / solusi wajib diisi')
    .min(10, 'Saran medis minimal harus 10 karakter')
})
