<template>
	<div
		v-if="event.title"
		class="flex flex-col h-full rounded-md shadow-md text-base overflow-auto"
		style="min-height: 320px"
	>
		<div
			class="event-image"
			:class="{ 'default-image': !event.image }"
			:style="{ backgroundImage: 'url(\'' + encodeURI(event.image) + '\')' }"
		>
			<div class="flex relative top-4 left-4 w-fit flex-wrap">
				<Badge
					v-if="event.featured"
					variant="subtle"
					theme="green"
					size="md"
					class="mr-2"
				>
					{{ __('Featured') }}
				</Badge>
				<Badge
					variant="outline"
					theme="gray"
					size="md"
					class="mr-2"
					v-for="tag in event.tags"
				>
					{{ tag }}
				</Badge>
			</div>
			<div v-if="!event.image" class="image-placeholder">
				{{ event.title[0] }}
			</div>
		</div>
		<div class="flex flex-col flex-auto p-4">
			<div class="flex items-center justify-between mb-2">
				<div v-if="event.lesson_count">
					<Tooltip :text="__('Lessons')">
						<span class="flex items-center">
							<BookOpen class="h-4 w-4 stroke-1.5 text-gray-700 mr-1" />
							{{ event.lesson_count }}
						</span>
					</Tooltip>
				</div>

				<div v-if="event.enrollment_count">
					<Tooltip :text="__('Enrolled Students')">
						<span class="flex items-center">
							<Users class="h-4 w-4 stroke-1.5 text-gray-700 mr-1" />
							{{ event.enrollment_count }}
						</span>
					</Tooltip>
				</div>

				<div v-if="event.avg_rating">
					<Tooltip :text="__('Average Rating')">
						<span class="flex items-center">
							<Star class="h-4 w-4 stroke-1.5 text-gray-700 mr-1" />
							{{ event.avg_rating }}
						</span>
					</Tooltip>
				</div>

				<div v-if="event.status != 'Approved'">
					<Badge
						variant="solid"
						:theme="event.status === 'Under Review' ? 'orange' : 'blue'"
						size="sm"
					>
						{{ event.status }}
					</Badge>
				</div>
			</div>

			<div class="text-xl font-semibold leading-6">
				{{ event.title }}
			</div>

			<div class="short-introduction">
				{{ event.short_introduction }}
			</div>

			<ProgressBar
				v-if="user && event.membership"
				:progress="event.membership.progress"
			/>

			<div v-if="user && event.membership" class="text-sm mb-4">
				{{ Math.ceil(event.membership.progress) }}% completed
			</div>

			<div class="flex items-center justify-between mt-auto">
				<div class="flex avatar-group overlap">
					<div
						class="h-6 mr-1"
						:class="{ 'avatar-group overlap': event.instructors.length > 1 }"
					>
						<UserAvatar
							v-for="instructor in event.instructors"
							:user="instructor"
						/>
					</div>
					<CourseInstructors :instructors="event.instructors" />
				</div>

				<div class="font-semibold">
					{{ event.price }}
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import { BookOpen, Users, Star } from 'lucide-vue-next'
import UserAvatar from '@/components/UserAvatar.vue'
import { sessionStore } from '@/stores/session'
import { Badge, Tooltip } from 'frappe-ui'
import CourseInstructors from '@/components/CourseInstructors.vue'
import ProgressBar from '@/components/ProgressBar.vue'

const { user } = sessionStore()

const props = defineProps({
	event: {
		type: Object,
		default: null,
	},
})
</script>
<style>
.event-image {
	height: 168px;
	width: 100%;
	background-size: cover;
	background-position: center;
	background-repeat: no-repeat;
}

.event-card-pills {
	background: #ffffff;
	margin-left: 0;
	margin-right: 0.5rem;
	padding: 3.5px 8px;
	font-size: 11px;
	text-align: center;
	letter-spacing: 0.011em;
	text-transform: uppercase;
	font-weight: 600;
	width: fit-content;
}

.default-image {
	display: flex;
	flex-direction: column;
	align-items: center;
	background-color: theme('colors.green.100');
	color: theme('colors.green.600');
}

.avatar-group {
	display: inline-flex;
	align-items: center;
}

.avatar-group .avatar {
	transition: margin 0.1s ease-in-out;
}
.image-placeholder {
	display: flex;
	align-items: center;
	flex: 1;
	font-size: 5rem;
	color: theme('colors.gray.700');
	font-weight: 600;
}
.avatar-group.overlap .avatar + .avatar {
	margin-left: calc(-8px);
}

.short-introduction {
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	text-overflow: ellipsis;
	width: 100%;
	overflow: hidden;
	margin: 0.25rem 0 1.25rem;
	line-height: 1.5;
}
</style>
