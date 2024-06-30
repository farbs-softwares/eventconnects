import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'

export const usersStore = defineStore('eventsconnect-users', () => {
	let userResource = createResource({
		url: 'eventsconnect.eventsconnect.api.get_user_info',
		onError(error) {
			if (error && error.exc_type === 'AuthenticationError') {
				router.push('/login')
			}
		},
		auto: true,
	})

	const allUsers = createResource({
		url: 'eventsconnect.eventsconnect.api.get_all_users',
		cache: ['allUsers'],
		auto: true,
	})

	return {
		userResource,
		allUsers,
	}
})
