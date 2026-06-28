import * as yup from 'yup'

export const aturanSchema = yup.object({
  penyakit_id: yup.string()
    .required('Penyakit wajib dipilih'),
  gejala_id: yup.string()
    .required('Gejala wajib dipilih'),
  conditional_probability: yup.number()
    .required('Bobot pakar wajib diisi')
    .typeError('Bobot pakar harus berupa angka')
    .min(0, 'Bobot pakar minimal 0.00')
    .max(1, 'Bobot pakar maksimal 1.00')
})
