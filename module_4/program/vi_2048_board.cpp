#include "vi_2048_board.h"

#include <algorithm>
#include <cstdio>

namespace vi
{
    std::vector<board::heuristic> board::heuristic_lut = board::build_heuristic_lut();
    board::move_luts              board::move_lut      = board::build_move_lut();
    std::vector<board::score>     board::score_lut     = board::build_score_lut();

    std::ostream&
    operator<<(std::ostream& os, const board& board)
    {
        for (unsigned row = 0; row != 4; ++row)
        {
            for (unsigned column = 0; column != 4; ++column)
            {
                printf("%5d ", board.get_value(row, column));
            }
            std::cout << std::endl;
        }
		return os;
    }

    std::vector<board::heuristic>
    board::build_heuristic_lut()
    {
        std::vector<board::heuristic> heuristic_lut(board::lut_size);

        const float SCORE_LOST_PENALTY        = 200000.0;
        const float SCORE_MONOTONICITY_POWER  = 4.0;
        const float SCORE_MONOTONICITY_WEIGHT = 47.0;
        const float SCORE_SUM_POWER           = 3.5;
        const float SCORE_SUM_WEIGHT          = 11.0;
        const float SCORE_MERGES_WEIGHT       = 700.0;
        const float SCORE_EMPTY_WEIGHT        = 270.0;

		for (unsigned row = 0; row < 65536; ++row)
        {
			unsigned line[4] = {
				(row >> 0) & 0xf,
				(row >> 4) & 0xf,
				(row >> 8) & 0xf,
				(row >> 12) & 0xf
			};

			int empty = 0;

			for (int i = 0; i < 4; ++i)
			{
				if (line[i] == 0)
				{
					++empty;
				}
			}

			const bool first_two  = line[0] && line[0] == line[1];
			const bool middle_two = line[1] && line[1] == line[2];
			const bool last_two   = line[2] && line[2] == line[3];
			const bool first_last = line[0] && line[0] == line[3] && line[1] == 0 && line[2] == 0;

			int num_merges = 0;
			int bad_tiles = 0;
			int second_merges = 0;
			int third_merges = 0;

			if (first_two && last_two)
			{
				num_merges = 2;
			}
			else if (first_two)
			{
				num_merges = 1;

				if (line[2])
				{
					if (line[2] == line[0] + 1)
					{
						second_merges = 1;

						if (line[3])
						{
							if (line[3] == line[2] + 1)
							{
								third_merges = 1;
							}
							else
							{
								++bad_tiles;
							}
						}
					}
					else
					{
						++bad_tiles;
						if (line[3])
						{
							++bad_tiles;
						}
					}
				}
				else
				{
					if (line[3])
					{
						if (line[3] == line[0] + 1)
						{
							second_merges = 1;
						}
						else
						{
							++bad_tiles;
						}
					}
				}
			}
			else if (last_two)
			{
				num_merges = 1;

				if (line[1])
				{
					if (line[1] == line[2] + 1)
					{
						second_merges = 1;

						if (line[0])
						{
							if (line[0] == line[1] + 1)
							{
								third_merges = 1;
							}
							else
							{
								++bad_tiles;
							}
						}
					}
					else
					{
						++bad_tiles;
						if (line[0])
						{
							++bad_tiles;
						}
					}
				}
				else
				{
					if (line[0])
					{
						if (line[3] == line[2] + 1)
						{
							second_merges = 1;
						}
						else
						{
							++bad_tiles;
						}
					}
				}
			}
			else if (middle_two)
			{
				num_merges = 1;
				if (line[0] == line[1] + 1)
				{
					++second_merges;
					if (line[3] == line[0] + 1)
					{
						++third_merges;
					}
					else if (line[3])
					{
						++bad_tiles;
					}
				}
				else if (line[3] == line[2] + 1)
				{
					++second_merges;
					if (line[0] == line[3] + 1)
					{
						++third_merges;
					}
					else if (line[0])
					{
						++bad_tiles;
					}
				}
				else
				{
					if (line[0])
					{
						++bad_tiles;
					}
					if (line[3])
					{
						++bad_tiles;
					}
				}
			}
			else if (first_last)
			{
				num_merges = 1;
			}
			else
			{
				for (int i = 0; i < 4; ++i)
				{
					if (line[i] != 0)
					{
						++bad_tiles;
					}
				}
			}

			heuristic_lut[row] = 10.0 + num_merges * 0.7 + 0.2 * second_merges + 0.1 * third_merges - pow(5, bad_tiles) / 100.0; //GOOD 15 min 4K @ depth 7
			//heuristic_lut[row] = 0.2 + num_merges * 0.5 + 0.2 * second_merges + 0.1 * third_merges - pow(2, bad_tiles) / 16.0; BAD
			//heuristic_lut[row] = 0.45 + num_merges * 0.2 + 0.1 * second_merges + 0.05 * third_merges - pow(2, bad_tiles) / 160.0; // ISH



			//heuristic_lut[row] = 10000 + 100 * num_merges
//				+ 50 * second_merges + 25 * third_merges;// -pow(5, bad_tiles);

			/*
			

			// Heuristic score
			float sum = 0;
			int empty = 0;
			int merges = 0;

			int prev = 0;
			int counter = 0;
			for (int i = 0; i < 4; ++i) {
				int rank = line[i];
				sum += pow(rank, SCORE_SUM_POWER);
				if (rank == 0) {
					empty++;
				}
				else {
					if (prev == rank) {
						counter++;
					}
					else if (counter > 0) {
						merges += 1 + counter;
						counter = 0;
					}
					prev = rank;
				}
			}
			if (counter > 0) {
				merges += 1 + counter;
			}

			float monotonicity_left = 0;
			float monotonicity_right = 0;
			for (int i = 1; i < 4; ++i) {
				if (line[i - 1] > line[i]) {
					monotonicity_left += pow(line[i - 1], SCORE_MONOTONICITY_POWER) - pow(line[i], SCORE_MONOTONICITY_POWER);
				}
				else {
					monotonicity_right += pow(line[i], SCORE_MONOTONICITY_POWER) - pow(line[i - 1], SCORE_MONOTONICITY_POWER);
				}
			}

			heuristic_lut[row] = empty;

			heuristic_lut[row] = SCORE_LOST_PENALTY +
				SCORE_EMPTY_WEIGHT * empty +
				SCORE_MERGES_WEIGHT * merges -
				SCORE_MONOTONICITY_WEIGHT * std::min(monotonicity_left, monotonicity_right) -
				SCORE_SUM_WEIGHT * sum;
			*/
        }

        return heuristic_lut;
    }

    board::move_luts
    board::build_move_lut()
    {
        board::move_luts move_lut{};

        move_lut.up    = std::vector<board::state>(board::lut_size);
        move_lut.down  = std::vector<board::state>(board::lut_size);
        move_lut.left  = std::vector<board::row>(board::lut_size);
        move_lut.right = std::vector<board::row>(board::lut_size);

        for (unsigned row = 0; row != board::lut_size; ++row)
        {
			/*
            board::row result        = 0;
            auto       output_offset = 0U;

            auto index = 0U;
            while (index < 3U)
            {
                const auto offset       = 4U * index;
                const auto current_cell = (row & (0xFU << offset)) >> offset;

                if (current_cell)
                {
                    const auto next_cell = (row & (0xFU << (offset + 4U))) >> (offset + 4);

                    if (current_cell == next_cell)
                    {
                        result |= (current_cell + 1U) << output_offset;
                        ++index;
                    }
                    else
                    {
                        result |= current_cell << output_offset;
                    }

                    output_offset += 4U;
                }

                ++index;
            }

            if (index < 4U)
            {
                const auto offset = 4U * index;
                result |= ((row & (0xFU << offset)) >> offset) << output_offset;
            }

            const auto rev_result   = reverse_row(result);
            const auto rev_row      = reverse_row(row);
			*/

			unsigned line[4] = {
				(row >> 0) & 0xf,
				(row >> 4) & 0xf,
				(row >> 8) & 0xf,
				(row >> 12) & 0xf
			};

			for (int i = 0; i < 3; ++i) {
				int j;
				for (j = i + 1; j < 4; ++j) {
					if (line[j] != 0) break;
				}
				if (j == 4) break; // no more tiles to the right

				if (line[i] == 0) {
					line[i] = line[j];
					line[j] = 0;
					i--; // retry this entry
				}
				else if (line[i] == line[j]) {
					if (line[i] != 0xf) {
						/* Pretend that 32768 + 32768 = 32768 (representational limit). */
						line[i]++;
					}
					line[j] = 0;
				}
			}

			auto result = (line[0] << 0) |
				(line[1] << 4) |
				(line[2] << 8) |
				(line[3] << 12);
			auto rev_result = reverse_row(result);
			unsigned rev_row = reverse_row(row);

            move_lut.up[row]        = unpack_column(row)     ^ unpack_column(result);
            move_lut.down[rev_row]  = unpack_column(rev_row) ^ unpack_column(rev_result);
            move_lut.left[row]      = row     ^ result;
            move_lut.right[rev_row] = rev_row ^ rev_result;
        }

        return move_lut;
    }

    std::vector<board::score>
    board::build_score_lut()
    {
        std::vector<board::score> score_lut(board::lut_size);

        for (auto row = 0U; row != board::lut_size; ++row)
        {
            board::score score{};

            for (auto i = 0U; i != 4; ++i)
            {
                const auto rank = (row >> (4U * i)) & 0xFU;
                if (rank >= 2)
                {
                    score += (rank - 1) * (1 << rank);
                }
            }

            score_lut[row] = score;
        }

        return score_lut;
    }
}
