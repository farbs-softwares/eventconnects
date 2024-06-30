<template>
	<div class="shadow rounded-md min-w-80">
		<iframe
			v-if="event.data.video_link"
			:src="video_link"
			class="rounded-t-md min-h-56 w-full"
		/>
		<div class="p-5">
			<div v-if="event.data.price" class="text-2xl font-semibold mb-3">
				{{ event.data.price }}
			</div>
			<router-link
				v-if="event.data.membership"
				:to="{
					name: 'Lesson',
					params: {
						eventName: event.name,
						chapterNumber: event.data.current_lesson
							? event.data.current_lesson.split('-')[0]
							: 1,
						lessonNumber: event.data.current_lesson
							? event.data.current_lesson.split('-')[1]
							: 1,
					},
				}"
			>
				<Button variant="solid" size="md" class="w-full">
					<span>
						{{ __('Continue Learning') }}
					</span>
				</Button>
			</router-link>
			<router-link
				v-else-if="event.data.paid_event"
				:to="{
					name: 'Billing',
					params: {
						type: 'event',
						name: event.data.name,
					},
				}"
			>
				<Button variant="solid" size="md" class="w-full">
					<span>
						{{ __('Buy this event') }}
					</span>
				</Button>
			</router-link>
			<div
				v-else-if="event.data.disable_self_learning"
				class="bg-blue-100 text-blue-900 text-sm rounded-md py-1 px-3"
			>
				{{ __('Contact the Administrator to enroll for this event.') }}
			</div>
			<Button
				v-else
				@click="enrollStudent()"
				variant="solid"
				class="w-full"
				size="md"
			>
				<span>
					{{ __('Start Learning') }}
				</span>
			</Button>
			<router-link
				v-if="user?.data?.is_moderator || is_instructor()"
				:to="{
					name: 'CreateCourse',
					params: {
						eventName: event.data.name,
					},
				}"
			>
				<Button variant="subtle" class="w-full mt-2" size="md">
					<span>
						{{ __('Edit') }}
					</span>
				</Button>
			</router-link>
			<div class="mt-8 mb-4 font-medium">
				{{ __('This event has:') }}
			</div>
			<div class="flex items-center mb-3">
				<BookOpen class="h-5 w-5 stroke-1.5 text-gray-600" />
				<span class="ml-2">
					{{ event.data.lesson_count }} {{ __('Lessons') }}
				</span>
			</div>
			<div class="flex items-center mb-3">
				<Users class="h-5 w-5 stroke-1.5 text-gray-600" />
				<span class="ml-2">
					{{ event.data.enrollment_count_formatted }}
					{{ __('Enrolled Students') }}
				</span>
			</div>
			<div class="flex items-center">
				<Star class="h-5 w-5 stroke-1.5 fill-orange-500 text-gray-50" />
				<span class="ml-2">
					{{ event.data.avg_rating }} {{ __('Rating') }}
				</span>
			</div>
		</div>
	</div>
</template>
<script setup>
import { BookOpen, Users, Star } from 'lucide-vue-next'
import { computed, inject } from 'vue'
import { Button, createResource } from 'frappe-ui'
import { createToast } from '@/utils/'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = inject('$user')

const props = defineProps({
	event: {
		type: Object,
		default: null,
	},
})

const video_link = computed(() => {
	if (props.event.data.video_link) {
		return 'https://www.youtube.com/embed/' + props.event.data.video_link
	}
	return null
})

function enrollStudent() {
	if (!user.data) {
		createToast({
			title: 'Please Login',
			icon: 'alert-circle',
			iconClasses: 'text-yellow-600 bg-yellow-100',
		})
		setTimeout(() => {
			window.location.href = `/login?redirect-to=${window.location.pathname}`
		}, 3000)
	} else {
		const enrollStudentResource = createResource({
			url: 'eventsconnect.eventsconnect.doctype.eventsconnect_enrollment.eventsconnect_enrollment.create_membership',
		})
		enrollStudentResource
			.submit({
				event: props.event.data.name,
			})
			.then(() => {
				createToast({
					title: 'Enrolled Successfully',
					icon: 'check',
					iconClasses: 'text-green-600 bg-green-100',
				})
				setTimeout(() => {
					router.push({
						name: 'Lesson',
						params: {
							eventName: props.event.data.name,
							chapterNumber: 1,
							lessonNumber: 1,
						},
					})
				}, 3000)
			})
	}
}

const is_instructor = () => {
	let user_is_instructor = false
	props.event.data.instructors.forEach((instructor) => {
		if (!user_is_instructor && instructor.name == user.data?.name) {
			user_is_instructor = true
		}
	})
	return user_is_instructor
}
</script>
