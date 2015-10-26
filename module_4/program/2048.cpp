#include "ai.h"
#include "board.h"

#include <iostream>
#include <random>


std::default_random_engine rng{std::random_device{}()};
auto tile_distribution = std::uniform_int_distribution<vi::board::state>{1, 10};

static inline
vi::board
insert_tile(vi::board board, vi::board::state tile, unsigned index)
{
    vi::board::state board_state = board.board_state;

    for (;; --index)
    {
        while (board_state & 0xFU)
        {
            board_state >>= 4;
            tile        <<= 4;
        }

        if (!index)
        {
            break;
        }

        board_state >>= 4;
        tile        <<= 4;
    }

    return vi::board{board.board_state | tile};
}

static inline
vi::board::state
random_tile()
{
    return tile_distribution(rng) == 10 ? 2 : 1;
}

int main()
{
    vi::ai ai{};

    vi::board board = insert_tile(
        vi::board{}, random_tile(), std::uniform_int_distribution<unsigned>{0, 15}(rng));

	auto move_count = 0;

    while (true)
    {
        int a = 0;
        for (; a != 4; ++a)
        {
            const auto move = static_cast<vi::action>(a);
            if (board.move(move) != board)
            {
                break;
            }
        }
        if (a == 4)
        {
            break;
        }

        auto move = ai.find_move(board);

		printf("Current: %.2f Actual: %.0f Moves: %d Moves evaluated: %d Move %d. Cache %d hits / %d misses (%.2f%%). Pruned %d hits / %d misses (%.2f%%)\n",
			board.get_heuristic(),
			board.get_score(),
			move_count,
			ai.moves_evaluated,
			static_cast<int>(move),
			ai.cache_hits,
			ai.cache_misses,
			100.0 * ai.cache_hits / (ai.cache_hits + ai.cache_misses),
			ai.probability_prune_hits,
			ai.probability_prune_misses,
			100.0 * ai.probability_prune_hits / (ai.probability_prune_hits + ai.probability_prune_misses));

		ai.moves_evaluated = 0;
		ai.cache_hits = 0;
		ai.cache_misses = 0;
		ai.probability_prune_hits = 0;
		ai.probability_prune_misses = 0;
		ai.transposition_table.clear();

        board = board.move(move);

		++move_count;

        auto num_available = board.get_available_count();
        if (num_available)
        {
            board = insert_tile(board,
                                random_tile(),
                                std::uniform_int_distribution<unsigned>{0, num_available - 1}(rng));
        }

        std::cout << board << std::endl;
    }

    std::cout << "GAME OVER! FINAL SCORE = " << board.get_score() << std::endl;
	getchar();
}
