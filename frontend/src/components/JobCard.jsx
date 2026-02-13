// import React from 'react';
// import { MapPin, Briefcase, DollarSign, TrendingUp } from 'lucide-react';

// const JobCard = ({ job }) => {
//   const matchPercentage = (job.similarity_score * 100).toFixed(1);
  
//   const getMatchColor = (score) => {
//     if (score >= 0.7) return 'text-green-600 bg-green-50';
//     if (score >= 0.5) return 'text-yellow-600 bg-yellow-50';
//     return 'text-orange-600 bg-orange-50';
//   };

//   return (
//     <div className="card hover:scale-[1.02] transition-transform cursor-pointer">
//       <div className="flex justify-between items-start mb-3">
//         <div>
//           <h3 className="text-xl font-bold text-white-800">{job.title}</h3>
//           <p className="text-blue-600 font-semibold">{job.company}</p>
//         </div>
        
//         <div className={`px-3 py-1 rounded-full ${getMatchColor(job.similarity_score)}`}>
//           <div className="flex items-center space-x-1">
//             <TrendingUp className="h-4 w-4" />
//             <span className="font-bold">{matchPercentage}%</span>
//           </div>
//         </div>
//       </div>

//       <div className="space-y-2 mb-4">
//         {job.location && (
//           <div className="flex items-center space-x-2 text-gray-200">
//             <MapPin className="h-4 w-4" />
//             <span>{job.location}</span>
//           </div>
//         )}
        
//         <div className="flex items-center space-x-2 text-gray-200">
//           <Briefcase className="h-4 w-4" />
//           <span>{job.job_type}</span>
//         </div>
        
//         {job.salary_range && (
//           <div className="flex items-center space-x-2 text-gray-200">
//             <DollarSign className="h-4 w-4" />
//             <span>{job.salary_range}</span>
//           </div>
//         )}
//       </div>

//       <p className="text-gray-200 text-sm line-clamp-3 mb-4">
//         {job.description}
//       </p>

//       {job.matched_skills && job.matched_skills.length > 0 && (
//         <div className="border-t pt-3">
//           <p className="text-sm font-semibold text-gray-700 mb-2">Matched Skills:</p>
//           <div className="flex flex-wrap gap-2">
//             {job.matched_skills.slice(0, 5).map((skill, index) => (
//               <span
//                 key={index}
//                 className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium"
//               >
//                 {skill}
//               </span>
//             ))}
//             {job.matched_skills.length > 5 && (
//               <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
//                 +{job.matched_skills.length - 5} more
//               </span>
//             )}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default JobCard;



import React, { useState, useEffect } from 'react';
import { MapPin, Briefcase, DollarSign, TrendingUp, Send, CheckCircle, Clock } from 'lucide-react';
import { applyToJob, checkApplicationStatus } from '../services/api';

const JobCard = ({ job, selectedResumeId }) => {
  const [applying, setApplying] = useState(false);
  const [applicationStatus, setApplicationStatus] = useState(null);
  const [hasApplied, setHasApplied] = useState(false);

  const matchPercentage = (job.similarity_score * 100).toFixed(1);
  
  const getMatchColor = (score) => {
    if (score >= 0.7) return 'from-green-500 to-emerald-500';
    if (score >= 0.5) return 'from-yellow-500 to-orange-500';
    return 'from-orange-500 to-red-500';
  };

  useEffect(() => {
    checkIfApplied();
  }, [job.id]);

  const checkIfApplied = async () => {
    try {
      const response = await checkApplicationStatus(job.id);
      setHasApplied(response.has_applied);
      setApplicationStatus(response.status);
    } catch (error) {
      console.error('Error checking application status:', error);
    }
  };

  const handleApply = async () => {
    if (!selectedResumeId) {
      alert('Please upload a resume first');
      return;
    }

    setApplying(true);
    try {
      await applyToJob({
        job_id: job.id,
        resume_id: selectedResumeId
      });
      setHasApplied(true);
      setApplicationStatus('pending');
      alert('Application submitted successfully!');
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to apply');
    } finally {
      setApplying(false);
    }
  };

  const getStatusBadge = () => {
    const statusConfig = {
      pending: { color: 'from-yellow-500 to-orange-500', text: 'Pending Review', icon: Clock },
      reviewed: { color: 'from-blue-500 to-cyan-500', text: 'Reviewed', icon: CheckCircle },
      shortlisted: { color: 'from-green-500 to-emerald-500', text: 'Shortlisted', icon: CheckCircle },
      rejected: { color: 'from-red-500 to-pink-500', text: 'Not Selected', icon: Clock }
    };

    const config = statusConfig[applicationStatus] || statusConfig.pending;
    const Icon = config.icon;

    return (
      <div className={`px-4 py-2 rounded-xl bg-gradient-to-r ${config.color}/20 border border-current/30 flex items-center gap-2`}>
        <Icon className="h-4 w-4" />
        <span className="font-semibold text-sm">{config.text}</span>
      </div>
    );
  };

  return (
    <div className="card glow-effect hover:scale-[1.01] transition-all duration-500 group">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-2xl font-bold text-white group-hover:text-red-300 transition-colors">
            {job.title}
          </h3>
          <p className="text-red-400 font-semibold text-lg mt-1">{job.company}</p>
        </div>
        
        <div className={`px-4 py-2 rounded-xl bg-gradient-to-r ${getMatchColor(job.similarity_score)}/20 border border-current/30`}>
          <div className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5" />
            <span className="font-bold text-lg">{matchPercentage}%</span>
          </div>
        </div>
      </div>

      <div className="space-y-3 mb-4">
        {job.location && (
          <div className="flex items-center space-x-2 text-gray-300">
            <MapPin className="h-4 w-4 text-red-400" />
            <span>{job.location}</span>
          </div>
        )}
        
        <div className="flex items-center space-x-2 text-gray-300">
          <Briefcase className="h-4 w-4 text-red-400" />
          <span>{job.job_type}</span>
        </div>
        
        {job.salary_range && (
          <div className="flex items-center space-x-2 text-gray-300">
            <DollarSign className="h-4 w-4 text-red-400" />
            <span>{job.salary_range}</span>
          </div>
        )}
      </div>

      <p className="text-gray-300 text-sm line-clamp-3 mb-4 leading-relaxed">
        {job.description}
      </p>

      {job.matched_skills && job.matched_skills.length > 0 && (
        <div className="border-t border-gray-800 pt-4 mb-4">
          <p className="text-sm font-semibold text-gray-400 mb-3">Matched Skills:</p>
          <div className="flex flex-wrap gap-2">
            {job.matched_skills.slice(0, 5).map((skill, index) => (
              <span
                key={index}
                className="px-3 py-1.5 bg-gradient-to-r from-red-900/40 to-pink-900/40 text-red-300 rounded-lg text-xs font-medium border border-red-800/30 hover:scale-105 transition-all"
              >
                {skill}
              </span>
            ))}
            {job.matched_skills.length > 5 && (
              <span className="px-3 py-1.5 bg-gradient-to-r from-gray-800 to-gray-900 text-gray-400 rounded-lg text-xs border border-gray-700">
                +{job.matched_skills.length - 5} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Application Status or Apply Button */}
      <div className="border-t border-gray-800 pt-4">
        {hasApplied ? (
          <div className="flex items-center justify-between">
            <span className="text-gray-400 text-sm">Application Status:</span>
            {getStatusBadge()}
          </div>
        ) : (
          <button
            onClick={handleApply}
            disabled={applying}
            className="w-full group/btn relative overflow-hidden bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 disabled:from-gray-700 disabled:to-gray-800 text-white font-bold py-3 px-6 rounded-xl transition-all duration-300 transform hover:-translate-y-1 disabled:transform-none disabled:cursor-not-allowed"
          >
            <span className="relative z-10 flex items-center justify-center gap-2">
              {applying ? (
                <>
                  <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Applying...
                </>
              ) : (
                <>
                  <Send className="h-5 w-5" />
                  Apply Now
                </>
              )}
            </span>
            <div className="absolute inset-0 bg-gradient-to-r from-pink-600/20 to-red-600/20 translate-x-full group-hover/btn:translate-x-0 transition-transform duration-500"></div>
          </button>
        )}
      </div>
    </div>
  );
};

export default JobCard;