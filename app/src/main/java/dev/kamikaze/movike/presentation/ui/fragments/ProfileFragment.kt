package dev.kamikaze.movike.presentation.ui.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.viewModels
import androidx.lifecycle.ViewModelProvider
import dev.kamikaze.movike.R
import dev.kamikaze.movike.common.base.BaseFragment
import dev.kamikaze.movike.databinding.FragmentProfileBinding
import dev.kamikaze.movike.presentation.navigation.navigators.ProfileNavigator
import dev.kamikaze.movike.presentation.ui.viewmodel.ProfileViewModel
import javax.inject.Inject

class ProfileFragment : BaseFragment<ProfileNavigator>() {

    @Inject
    lateinit var factory: ViewModelProvider.Factory
    private val viewModel: ProfileViewModel by viewModels { factory }

    private var _binding: FragmentProfileBinding? = null
    private val binding: FragmentProfileBinding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentProfileBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onResume() {
        super.onResume()
        setTitle(R.string.profile_title)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    override fun initView() {

    }

    override fun onRetryLoad() {

    }

}
