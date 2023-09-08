import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const userApi = createApi({
    reducerPath: 'userApi',
    baseQuery: fetchBaseQuery({
        baseUrl: "/",
    }),
    tagTypes: ['User'],
    endpoints(builder){
        return {
            autoLogin: builder.query({
                query: () => '/authorized',
                providesTags: ['User'],
            }),
            createUser: builder.mutation({
                query: ({...body}) => ({
                    url: '/signup',
                    method: 'POST',
                    body
                }),
                invalidatesTags: ['User'],
            }),

        }
    }
})

export const { useAutoLoginQuery, useCreateUserMutation } = userApi