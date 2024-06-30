<template>
	<div v-if="events.data">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs
				class="h-7"
				:items="[{ label: __('All Courses'), route: { name: 'Courses' } }]"
			/>
			<div class="flex space-x-2">
				<FormControl
					type="text"
					placeholder="Search Event"
					v-model="searchQuery"
					@input="events.reload()"
				>
					<template #prefix>
						<Search class="w-4 stroke-1.5 text-gray-600" name="search" />
					</template>
				</FormControl>
				<router-link
					:to="{
						name: 'CreateCourse',
						params: {
							eventName: 'new',
						},
					}"
				>
					<Button v-if="user.data?.is_moderator" variant="solid">
						<template #prefix>
							<Plus class="h-4 w-4" />
						</template>
						{{ __('New Event') }}
					</Button>
				</router-link>
			</div>
		</header>
		<div class="">
			<Tabs
				v-model="tabIndex"
				tablistClass="overflow-x-visible flex-wrap !gap-3 md:flex-nowrap"
				:tabs="tabs"
			>
				<template #tab="{ tab, selected }">
					<div>
						<button
							class="group -mb-px flex items-center gap-2 overflow-hidden border-b border-transparent py-2.5 text-base text-gray-600 duration-300 ease-in-out hover:border-gray-400 hover:text-gray-900"
							:class="{ 'text-gray-900': selected }"
						>
							<component v-if="tab.icon" :is="tab.icon" class="h-5" />
							{{ __(tab.label) }}
							<Badge theme="gray">
								{{ tab.count }}
							</Badge>
						</button>
					</div>
				</template>
				<template #default="{ tab }">
					<div
						v-if="tab.events && tab.events.value.length"
						class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 my-5 mx-5"
					>
						<router-link
							v-for="event in tab.events.value"
							:to="
								event.membership && event.current_lesson
									? {
											name: 'Lesson',
											params: {
												eventName: event.name,
												chapterNumber: event.current_lesson.split('-')[0],
												lessonNumber: event.current_lesson.split('-')[1],
											},
									  }
									: event.membership
									? {
											name: 'Lesson',
											params: {
												eventName: event.name,
												chapterNumber: 1,
												lessonNumber: 1,
											},
									  }
									: {
											name: 'CourseDetail',
											params: { eventName: event.name },
									  }
							"
						>
							<CourseCard :event="event" />
						</router-link>
					</div>
					<div
						v-else
						class="grid flex-1 place-items-center text-xl font-medium text-gray-500"
					>
						<div class="flex flex-col items-center justify-center mt-4">
							<div>
								{{ __('No {0} events found').format(tab.label.toLowerCase()) }}
							</div>
						</div>
					</div>
				</template>
			</Tabs>
		</div>
	</div>
</template>

<script setup>
import {
	Breadcrumbs,
	Tabs,
	Badge,
	Button,
	FormControl,
	createResource,
} from 'frappe-ui'
import CourseCard from '@/components/CourseCard.vue'
import { Plus, Search } from 'lucide-vue-next'
import { ref, computed, inject } from 'vue'
import { updateDocumentTitle } from '@/utils'

const user = inject('$user')
const searchQuery = ref('')

const events = createResource({
	debounce: 300,
	makeParams(values) {
		return {
			search_query: searchQuery.value,
		}
	},
	url: 'eventsconnect.eventsconnect.utils.get_events',
	auto: true,
})

const tabIndex = ref(0)
const tabs = [
	{
		label: 'Live',
		events: computed(() => events.data?.live || []),
		count: computed(() => events.data?.live?.length),
	},
	{
		label: 'New',
		events: computed(() => events.data?.new),
		count: computed(() => events.data?.new?.length),
	},
	{
		label: 'Upcoming',
		events: computed(() => events.data?.upcoming),
		count: computed(() => events.data?.upcoming?.length),
	},
]

if (user.data) {
	tabs.push({
		label: 'Enrolled',
		events: computed(() => events.data?.enrolled),
		count: computed(() => events.data?.enrolled?.length),
	})

	if (
		user.data.is_moderator ||
		user.data.is_instructor ||
		events.data?.created?.length
	) {
		tabs.push({
			label: 'Created',
			events: computed(() => events.data?.created),
			count: computed(() => events.data?.created?.length),
		})
	}

	if (user.data.is_moderator) {
		tabs.push({
			label: 'Under Review',
			events: computed(() => events.data?.under_review),
			count: computed(() => events.data?.under_review?.length),
		})
	}
}

const pageMeta = computed(() => {
	return {
		title: 'Courses',
		description: 'All Courses divided by categories',
	}
})

updateDocumentTitle(pageMeta)
</script>
