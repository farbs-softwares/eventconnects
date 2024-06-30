<template>
	<div class="mt-7">
		<h2 class="mb-3 text-lg font-semibold text-gray-900">
			{{ __('Settings') }}
		</h2>
		<div
			class="flex flex-col md:flex-row gap-4 md:gap-0 justify-between w-3/4 mt-5"
		>
			<FormControl
				:label="__('Moderator')"
				v-model="moderator"
				type="checkbox"
				@change.stop="changeRole('moderator')"
			/>
			<FormControl
				:label="__('Event Creator')"
				v-model="event_creator"
				type="checkbox"
				@change.stop="changeRole('event_creator')"
			/>
			<FormControl
				:label="__('Evaluator')"
				v-model="batch_evaluator"
				type="checkbox"
				@change.stop="changeRole('batch_evaluator')"
			/>
			<FormControl
				:label="__('Student')"
				v-model="eventsconnect_student"
				type="checkbox"
				@change.stop="changeRole('eventsconnect_student')"
			/>
		</div>
	</div>
</template>
<script setup>
import { FormControl, createResource } from 'frappe-ui'
import { ref } from 'vue'
import { showToast, convertToTitleCase } from '@/utils'

const moderator = ref(false)
const event_creator = ref(false)
const batch_evaluator = ref(false)
const eventsconnect_student = ref(false)

const props = defineProps({
	profile: {
		type: Object,
		required: true,
	},
})

const roles = createResource({
	url: 'eventsconnect.eventsconnect.utils.get_roles',
	makeParams(values) {
		return {
			name: props.profile.data?.name,
		}
	},
	auto: true,
	onSuccess(data) {
		let roles = [
			'moderator',
			'event_creator',
			'batch_evaluator',
			'eventsconnect_student',
		]
		for (let role of roles) {
			if (data[role]) eval(role).value = true
		}
	},
})

const updateRole = createResource({
	url: 'eventsconnect.overrides.user.save_role',
	makeParams(values) {
		return {
			user: props.profile.data?.name,
			role: values.role,
			value: values.value,
		}
	},
})

const changeRole = (role) => {
	updateRole.submit(
		{
			role: convertToTitleCase(role.split('_').join(' ')),
			value: eval(role).value,
		},
		{
			onSuccess(data) {
				showToast('Success', 'Role updated successfully', 'check')
			},
		}
	)
}
</script>
