import { createI18n } from 'vue-i18n'

export const messages = {
  en: {
    landing: {
      features: 'Features',
      plans: 'Plans',
      sign_up: 'Sign up',
      log_in: 'Log in',
      heroTitle: 'Protect against customer Churn',
      heroDescription:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis mollis lacus non massa fringilla, id volutpat massa sagittis. Etiam porttitor eros nec porta molestie. Donec blandit tempor mattis. Aliquam erat volutpat. Praesent eget arcu purus. Integer nec nibh ut neque condimentum tempus. Praesent sagittis turpis in lobortis vulputate.',
      heroButton: 'Get started!',
      featureOneTitle: 'Feature 1',
      featureOneDescription: 'Feature 2',
      featureTwoTitle: 'Feature 3',
      featureTwoDescription:
        'Sed ut tincidunt eros. Morbi sollicitudin felis ac augue mattis cursus. Praesent nisl felis, interdum eget sapien ac, euismod fermentum diam. Morbi eu velit odio. ',
      featureThreeTitle:
        'Sed ut tincidunt eros. Morbi sollicitudin felis ac augue mattis cursus. Praesent nisl felis, interdum eget sapien ac, euismod fermentum diam. Morbi eu velit odio. ',
      featureThreeDescription:
        'Sed ut tincidunt eros. Morbi sollicitudin felis ac augue mattis cursus. Praesent nisl felis, interdum eget sapien ac, euismod fermentum diam. Morbi eu velit odio. ',
    },
    login: {
      title: 'Login to your account',
      email: 'Email',
      password: 'Password',
      remember: 'Remember Me',
      action: 'Login',
      reminder: "Don't have an account?",
    },
    register: {
      title: 'Create an account',
      username: 'Username',
      email: 'Email',
      password: 'Password',
      confirm: 'Confirm password',
      remember: 'Remember Me',
      action: 'Sign up',
      reminder: 'Already have an account?',
    },
  },
  ar: {},

  fr: {},
} as const

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages,
})
