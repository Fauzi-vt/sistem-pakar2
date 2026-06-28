import * as yup from 'yup'

export const registerSchema = yup.object({
  name: yup.string()
    .required('Nama lengkap wajib diisi')
    .min(3, 'Nama lengkap minimal harus 3 karakter'),
  email: yup.string()
    .required('Email wajib diisi')
    .email('Format email tidak valid'),
  password: yup.string()
    .required('Kata sandi wajib diisi')
    .min(6, 'Kata sandi minimal harus 6 karakter'),
  confirm: yup.string()
    .required('Konfirmasi kata sandi wajib diisi')
    .oneOf([yup.ref('password'), null], 'Konfirmasi kata sandi tidak cocok'),
  agreeTerms: yup.boolean()
    .oneOf([true], 'Anda harus menyetujui Syarat dan Ketentuan')
})
