import * as yup from 'yup'

export const loginSchema = yup.object({
  email: yup.string()
    .required('Email wajib diisi')
    .email('Format email tidak valid'),
  password: yup.string()
    .required('Kata sandi wajib diisi')
    .min(6, 'Kata sandi minimal harus 6 karakter')
})
