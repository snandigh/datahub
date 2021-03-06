import { useMemo } from 'react';
import { QueryResult } from '@apollo/client';
import { EntityType, Exact, SearchInput } from '../../types.generated';
import { GetSearchResultsQuery, useGetSearchResultsQuery } from '../../graphql/search.generated';
import { useEntityRegistry } from '../../app/useEntityRegistry';

type GetAllSearchResults<K> = Record<EntityType, K>;
type AllEntityInput<T, K> = Pick<T, Exclude<keyof T, keyof K>> & K;

export type GetAllEntitySearchResultsType = GetAllSearchResults<
    QueryResult<GetSearchResultsQuery, Exact<{ input: SearchInput }>>
>;

export function useGetAllEntitySearchResults(
    input: AllEntityInput<SearchInput, { type?: EntityType }>,
): GetAllEntitySearchResultsType {
    const result: {
        [key in EntityType]: QueryResult<
            GetSearchResultsQuery,
            Exact<{
                input: SearchInput;
            }>
        >;
    } = {} as {
        [key in EntityType]: QueryResult<
            GetSearchResultsQuery,
            Exact<{
                input: SearchInput;
            }>
        >;
    };
    const entityRegistry = useEntityRegistry();

    const searchTypes = entityRegistry.getSearchEntityTypes();

    for (let i = 0; i < searchTypes.length; i++) {
        const type = searchTypes[i];
        // eslint-disable-next-line react-hooks/rules-of-hooks
        result[type] = useGetSearchResultsQuery({
            variables: {
                input: {
                    type,
                    ...input,
                },
            },
        });
    }

    return useMemo(
        () => result,
        // eslint-disable-next-line react-hooks/exhaustive-deps
        Object.keys(result).map((key) => result[key]),
    );
}
