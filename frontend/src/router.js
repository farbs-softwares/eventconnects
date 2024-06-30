import { createRouter, createWebHistory } from 'vue-router'
import { usersStore } from './stores/user'
import { sessionStore } from './stores/session'

let defaultRoute = '/courses'
const routes = [
	{
		path: '/',
		redirect: {
			name: 'Courses',
		},
	},
	{
		path: '/courses',
		name: 'Courses',
		component: () => import('@/pages/Courses.vue'),
	},
	{
		path: '/courses/:courseName',
		name: 'CourseDetail',
		component: () => import('@/pages/CourseDetail.vue'),
		props: true,
	},
	{
		path: '/courses/:courseName/learn/:chapterNumber-:lessonNumber',
		name: 'Lesson',
		component: () => import('@/pages/Lesson.vue'),
		props: true,
	},
	{
		path: '/batches',
		name: 'Batches',
		component: () => import('@/pages/Batches.vue'),
	},
	{
		path: '/batches/details/:batchName',
		name: 'BatchDetail',
		component: () => import('@/pages/BatchDetail.vue'),
		props: true,
	},
	{
		path: '/batches/:batchName',
		name: 'Batch',
		component: () => import('@/pages/Batch.vue'),
		props: true,
	},
	{
		path: '/billing/:type/:name',
		name: 'Billing',
		component: () => import('@/pages/Billing.vue'),
		props: true,
	},
	{
		path: '/statistics',
		name: 'Statistics',
		component: () => import('@/pages/Statistics.vue'),
	},
	{
		path: '/user/:username',
		name: 'Profile',
		component: () => import('@/pages/Profile.vue'),
		props: true,
		redirect: { name: 'ProfileAbout' },
		children: [
			{
				name: 'ProfileAbout',
				path: '',
				component: () => import('@/pages/ProfileAbout.vue'),
			},
			{
				name: 'ProfileCertificates',
				path: 'certificates',
				component: () => import('@/pages/ProfileCertificates.vue'),
			},
			{
				name: 'ProfileRoles',
				path: 'roles',
				component: () => import('@/pages/ProfileRoles.vue'),
			},
			{
				name: 'ProfileEvaluator',
				path: 'evaluations',
				component: () => import('@/pages/ProfileEvaluator.vue'),
			},
		],
	},
	{
		path: '/eventjob-openings',
		name: 'EventJobs',
		component: () => import('@/pages/EventJobs.vue'),
	},
	{
		path: '/eventjob-openings/:eventjob',
		name: 'EventJobDetail',
		component: () => import('@/pages/EventJobDetail.vue'),
		props: true,
	},
	{
		path: '/courses/:courseName/edit',
		name: 'CreateCourse',
		component: () => import('@/pages/CreateCourse.vue'),
		props: true,
	},
	{
		path: '/courses/:courseName/learn/:chapterNumber-:lessonNumber/edit',
		name: 'CreateLesson',
		component: () => import('@/pages/CreateLesson.vue'),
		props: true,
	},
	{
		path: '/batches/:batchName/edit',
		name: 'BatchCreation',
		component: () => import('@/pages/BatchCreation.vue'),
		props: true,
	},
	{
		path: '/eventjob-opening/:eventjobName/edit',
		name: 'EventJobCreation',
		component: () => import('@/pages/EventJobCreation.vue'),
		props: true,
	},
	{
		path: '/assignment-submission/:assignmentName/:submissionName',
		name: 'AssignmentSubmission',
		component: () => import('@/pages/AssignmentSubmission.vue'),
		props: true,
	},
	{
		path: '/certified-participants',
		name: 'CertifiedParticipants',
		component: () => import('@/pages/CertifiedParticipants.vue'),
	},
	{
		path: '/notifications',
		name: 'Notifications',
		component: () => import('@/pages/Notifications.vue'),
	},
	{
		path: '/badges/:badgeName/:email',
		name: 'Badge',
		component: () => import('@/pages/Badge.vue'),
		props: true,
	},
]

let router = createRouter({
	history: createWebHistory('/eventsconnect'),
	routes,
})

router.beforeEach(async (to, from, next) => {
	const { userResource, allUsers } = usersStore()
	let { isLoggedIn } = sessionStore()

	try {
		if (isLoggedIn) {
			await userResource.promise
		}
		if (
			isLoggedIn &&
			(to.name == 'Lesson' ||
				to.name == 'Batch' ||
				to.name == 'Notifications' ||
				to.name == 'Badge')
		) {
			await allUsers.promise
		}
	} catch (error) {
		isLoggedIn = false
	}
	return next()
})

export default router
